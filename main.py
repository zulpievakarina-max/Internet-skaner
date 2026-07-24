import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class NetworkScannerApp(App):
    def build(self):
        self.is_scanning = False

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Заголовок
        self.title_label = Label(
            text="[b]TOR SKANERI[/b]", 
            markup=True, 
            font_size='22sp', 
            size_hint_y=None, 
            height=40
        )
        layout.add_widget(self.title_label)

        # IP информация
        local_ip = self.get_local_ip()
        ip_prefix = ".".join(local_ip.split(".")[:-1]) + "."
        
        self.info_label = Label(
            text=f"IP: {local_ip} | Aralyk: {ip_prefix}1 - {ip_prefix}254", 
            font_size='14sp', 
            size_hint_y=None, 
            height=30
        )
        layout.add_widget(self.info_label)

        # Кнопки
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.scan_btn = Button(
            text="Başlat", 
            background_color=(0.3, 0.8, 0.3, 1),
            bold=True
        )
        self.scan_btn.bind(on_press=self.start_scan)
        btn_layout.add_widget(self.scan_btn)

        self.clear_btn = Button(
            text="Arassala", 
            background_color=(0.9, 0.3, 0.3, 1),
            bold=True
        )
        self.clear_btn.bind(on_press=self.clear_results)
        btn_layout.add_widget(self.clear_btn)

        layout.add_widget(btn_layout)

        # Поле результатов
        self.scroll = ScrollView()
        self.result_label = Label(
            text="", 
            font_size='13sp', 
            size_hint_y=None, 
            halign='left', 
            valign='top'
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.scroll.add_widget(self.result_label)
        layout.add_widget(self.scroll)

        return layout

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def append_result(self, text):
        def update_text(dt):
            self.result_label.text += text + "\n"
        Clock.schedule_once(update_text)

    def scan_ip(self, ip):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            result = s.connect_ex((ip, 80))
            if result == 0 or result == 111:
                self.append_result(f"[IŞJEŇ] {ip} --> İşjeň Enjam")
            s.close()
        except Exception:
            pass

    def scan_thread(self):
        local_ip = self.get_local_ip()
        ip_prefix = ".".join(local_ip.split(".")[:-1]) + "."
        
        threads = []
        for i in range(1, 255):
            if not self.is_scanning:
                break
            target_ip = f"{ip_prefix}{i}"
            t = threading.Thread(target=self.scan_ip, args=(target_ip,))
            threads.append(t)
            t.start()
            
            if len(threads) >= 50:
                for t in threads:
                    t.join()
                threads = []

        for t in threads:
            t.join()

        self.append_result("\nSkanirleme tamamlandy!")
        self.is_scanning = False
        def enable_btn(dt):
            self.scan_btn.disabled = False
        Clock.schedule_once(enable_btn)

    def start_scan(self, instance):
        if not self.is_scanning:
            self.is_scanning = True
            self.scan_btn.disabled = True
            self.result_label.text = ""
            threading.Thread(target=self.scan_thread).start()

    def clear_results(self, instance):
        self.result_label.text = ""

if __name__ == '__main__':
    NetworkScannerApp().run()
      
