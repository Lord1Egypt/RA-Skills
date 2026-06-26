import os
import threading
import pyaudio
import dashscope
from dashscope.audio.asr import *
from pynput import keyboard
from PIL import Image, ImageDraw
import pystray
from http import HTTPStatus

# --- 配置参数 ---
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY') or "你的API_KEY"
sample_rate = 16000
channels = 1
format_pcm = 'pcm'

kb_controller = keyboard.Controller()

class VoiceInputMethod:
    def __init__(self):
        self.recognition = None
        self.mic = None
        self.stream = None
        self.is_recording = False
        self._stop_event = threading.Event()
        
        # --- 核心状态：当前翻译模式 ---
        # 可选值: "OFF", "英语", "日语", "韩语", "德语", "法语" 等
        self.target_lang = "OFF" 

    def start_recording(self):
        if self.is_recording: return
        self.is_recording = True
        try:
            callback = MyRecognitionCallback(self)
            self.recognition = Recognition(
                model='fun-asr-realtime',
                format=format_pcm,
                sample_rate=sample_rate,
                semantic_punctuation_enabled=True,
                callback=callback
            )
            self.recognition.start()
            self.mic = pyaudio.PyAudio()
            self.stream = self.mic.open(format=pyaudio.paInt16, channels=channels,
                                        rate=sample_rate, input=True, frames_per_buffer=3200)
            self.send_thread = threading.Thread(target=self._worker)
            self.send_thread.start()
        except Exception as e:
            print(f"Error: {e}")
            self.is_recording = False

    def _worker(self):
        try:
            while self.is_recording:
                data = self.stream.read(3200, exception_on_overflow=False)
                self.recognition.send_audio_frame(data)
        finally:
            self.recognition.stop()

    def stop_recording(self):
        if not self.is_recording: return
        self.is_recording = False
        if hasattr(self, 'send_thread'): self.send_thread.join()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.mic: self.mic.terminate()

app = VoiceInputMethod()

def qwen_translate(text, target_lang):
    """根据 target_lang 进行翻译，如果是 OFF 则直接返回"""
    if target_lang == "OFF" or not text.strip():
        return text

    prompt = f"""Role: 你是一位精通中英文及多语种环境的同声传译专家。
Task: 请将以下 ASR 识别出的口语文本翻译成{target_lang}。
Requirement:
1. 如果 ASR 文本中有明显的口误或重复，请在翻译时自动修正。
2. 保持口语化的自然感。
3. 如果文本包含专业术语，请保持专业性。
4. 热词列表: ["FunASR", "Qwen LLM"]
Input: {text}"""

    try:
        response = dashscope.Generation.call(
            model='qwen-plus',
            prompt=prompt,
            result_format='message',
        )
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content.strip().strip('"')
        else:
            return text
    except Exception:
        return text

class MyRecognitionCallback(RecognitionCallback):
    def __init__(self, app_instance):
        super().__init__()
        self.app = app_instance

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            text = sentence['text']
            if RecognitionResult.is_sentence_end(sentence):
                # 异步处理：翻译 -> 打字
                threading.Thread(target=self._process, args=(text,)).start()

    def _process(self, raw_text):
        # 获取当前翻译设置
        mode = self.app.target_lang
        # 如果是 OFF，直接输出；否则调用 Qwen
        final_text = qwen_translate(raw_text, mode) if mode != "OFF" else raw_text
        
        try:
            kb_controller.type(final_text)
        except:
            pass

# --- 托盘图标逻辑 ---
def create_image():
    # 这里沿用你原来的绘制图标逻辑
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([5, 5, 59, 59], radius=15, fill=(255, 60, 0, 255))
    draw.rectangle([25, 15, 30, 45], fill=(255, 255, 255, 255))
    draw.rectangle([35, 20, 40, 40], fill=(255, 255, 255, 255))
    return img

def on_quit(icon, item):
    icon.stop()
    os._exit(0)

# 设置语言的动作
def set_lang(lang_name):
    def _action(icon, item):
        app.target_lang = lang_name
        print(f"切换模式至: {lang_name}")
    return _action

# 检查当前语言是否选中的逻辑
def is_lang_selected(lang_name):
    return lambda item: app.target_lang == lang_name

def run_tray():
    # 构建动态菜单
    menu = pystray.Menu(
        pystray.MenuItem("按住右侧⌥键说话 (Alt_R)", None, enabled=False),
        pystray.Menu.SEPARATOR,
        
        # 关闭翻译选项
        pystray.MenuItem(
            "关闭翻译 (仅输入法)", 
            set_lang("OFF"), 
            checked=is_lang_selected("OFF"), 
            radio=True
        ),
        
        # 各种语言选项
        pystray.MenuItem(
            "翻译为：中文", 
            set_lang("中文"), 
            checked=is_lang_selected("中文"), 
            radio=True
        ),
        pystray.MenuItem(
            "翻译为：英语", 
            set_lang("英语"), 
            checked=is_lang_selected("英语"), 
            radio=True
        ),
        pystray.MenuItem(
            "翻译为：日语", 
            set_lang("日语"), 
            checked=is_lang_selected("日语"), 
            radio=True
        ),
        pystray.MenuItem(
            "翻译为：韩语", 
            set_lang("韩语"), 
            checked=is_lang_selected("韩语"), 
            radio=True
        ),
        
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("退出", on_quit)
    )
    
    icon = pystray.Icon("FunVoiceType", create_image(), "fun-voice-type", menu=menu)
    icon.run()

# --- 键盘监听 ---
def on_press(key):
    if key == keyboard.Key.alt_r:
        app.start_recording()

def on_release(key):
    if key == keyboard.Key.alt_r:
        app.stop_recording()

if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    run_tray()
