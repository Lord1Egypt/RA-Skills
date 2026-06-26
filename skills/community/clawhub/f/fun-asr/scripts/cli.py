import os
import sys

import dashscope
import librosa
from dashscope.audio.asr import *


class Callback(RecognitionCallback):
    def __init__(self):
        self.final_text = None

    def on_complete(self) -> None:
        if self.final_text:
            print(self.final_text)

    def on_error(self, message) -> None:
        print(message.message, file=sys.stderr)
        sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if sentence and "text" in sentence:
            if RecognitionResult.is_sentence_end(sentence):
                self.final_text = sentence.get("text", "")


def read_audio_file(audio_path: str):
    """Read audio file and return PCM data.

    Supports various audio formats (wav, mp3, flac, ogg, etc.) via librosa.
    """
    data = librosa.load(audio_path, sr=16000, mono=True)[0]
    # Convert to int16 PCM
    data = (data * 32767).astype("int16")
    # Convert to bytes
    return data.tobytes()


if __name__ == "__main__":
    # Get audio file path from user
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        audio_file = input("请输入音频文件路径: ").strip()

    if not os.path.exists(audio_file):
        print(f"Error: 文件不存在: {audio_file}")
        sys.exit(1)

    dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
    dashscope.base_websocket_api_url = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"

    callback = Callback()
    recognition = Recognition(
        model="fun-asr-realtime",
        format="pcm",
        sample_rate=16000,
        semantic_punctuation_enabled=False,
        callback=callback,
    )
    # Start recognition
    recognition.start()
    # Read audio file and send all at once
    audio_data = read_audio_file(audio_file)
    recognition.send_audio_frame(audio_data)
    # Stop recognition
    recognition.stop()
