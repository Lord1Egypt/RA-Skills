import os
import sys
import subprocess
from pathlib import Path
from typing import Iterator, Tuple, List

from moonshine_voice import (
    Transcriber,
    TranscriptEventListener,
    get_model_for_language,
    load_wav_file,
    get_assets_path, # This might not be needed if we only process user provided audio files
)

class MoonshineASR:
    def __init__(self, language: str = "en"):
        self.language = language
        self.model_path, self.model_arch = get_model_for_language(self.language)
        self.transcriber = Transcriber(model_path=self.model_path, model_arch=self.model_arch)

    def speech_to_text(self, audio_file: str) -> str:
        try:
            processed_audio_file = audio_file
            # If OGG format, convert to WAV using ffmpeg
            if audio_file.endswith('.ogg'):
                wav_file = audio_file.replace('.ogg', '.wav')
                subprocess.run([
                    'ffmpeg', '-i', audio_file, '-ar', '16000', '-ac', '1',
                    '-f', 'wav', wav_file
                ], check=True, capture_output=True)
                processed_audio_file = wav_file

            audio_data, sample_rate = load_wav_file(processed_audio_file)

            # Define a simple event listener to capture the full transcript
            class FullTranscriptListener(TranscriptEventListener):
                def __init__(self):
                    self.full_transcript = []

                def on_line_completed(self, event):
                    self.full_transcript.append(event.line.text)

            listener = FullTranscriptListener()
            
            stream = self.transcriber.create_stream(update_interval=0.5)
            stream.add_listener(listener)
            stream.start()

            # Feed audio chunks into the stream.
            # Moonshine expects float samples, so convert if necessary.
            # Assuming load_wav_file returns float samples.
            chunk_size = int(0.1 * sample_rate) # 0.1 second chunks
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i: i + chunk_size]
                stream.add_audio(chunk, sample_rate) # Ensure chunk is a list

            stream.stop()
            stream.close()

            return " ".join(listener.full_transcript).strip()

        except Exception as e:
            print(f"Error during Moonshine ASR: {e}", file=sys.stderr)
            return ""

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 moonshine_asr_provider.py <audio_file>")
        print("Example: python3 moonshine_asr_provider.py input.ogg")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        print(f"❌ 音频文件不存在: {audio_file}")
        sys.exit(1)
    
    asr = MoonshineASR()
    text = asr.speech_to_text(audio_file)
    print(text)

if __name__ == "__main__":
    main()
