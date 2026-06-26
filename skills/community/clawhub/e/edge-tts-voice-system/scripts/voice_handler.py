#!/usr/bin/env python3
"""
OpenClaw Voice Handler
- Speech-to-Text: faster-whisper (offline)
- Text-to-Speech: Edge TTS (local)
"""
import subprocess
import tempfile
import os
import sys
import json

class VoiceHandler:
    def __init__(self):
        """Initialize voice handler with both STT and TTS"""
        self.stt_model = "base"  # faster-whisper model size
        self.tts_script = "/root/.openclaw/tts/tts_edge_wrapper.py"
        
    def audio_to_text(self, audio_file):
        """
        Transcribe audio file to text using faster-whisper
        
        Args:
            audio_file: Path to audio file (WAV, OGG, etc.)
        
        Returns:
            Transcribed text or error message
        """
        try:
            # Convert to WAV if needed
            if audio_file.endswith('.ogg'):
                wav_file = tempfile.mktemp(suffix=".wav")
                cmd = f"ffmpeg -i '{audio_file}' -ar 16000 -ac 1 '{wav_file}' -y 2>/dev/null"
                subprocess.run(cmd, shell=True, check=True)
                audio_file = wav_file
            
            # Transcribe with faster-whisper
            cmd = [
                sys.executable, "-c", """
from faster_whisper import WhisperModel
import sys
model = WhisperModel('%s', device='cpu', compute_type='int8')
segments, info = model.transcribe('%s', beam_size=5)
text = ' '.join(segment.text for segment in segments)
print(json.dumps({'text': text, 'language': info.language, 'probability': info.language_probability}))
""" % (self.stt_model, audio_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout.strip())
                return data['text'].strip()
            else:
                return f"Transcription error: {result.stderr}"
                
        except Exception as e:
            return f"Error in audio_to_text: {e}"
    
    def text_to_audio(self, text, output_file=None):
        """
        Convert text to audio using Edge TTS
        
        Args:
            text: Text to convert
            output_file: Output WAV file (optional)
        
        Returns:
            Path to generated audio file
        """
        try:
            if output_file is None:
                output_file = tempfile.mktemp(suffix=".wav", prefix="tts_")
            
            cmd = [sys.executable, self.tts_script, text, output_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_file):
                return output_file
            else:
                print(f"TTS error: {result.stderr}", file=sys.stderr)
                return None
                
        except Exception as e:
            print(f"Error in text_to_audio: {e}", file=sys.stderr)
            return None
    
    def process_voice_message(self, audio_file):
        """
        Complete voice message processing:
        1. Transcribe audio to text
        2. Generate response (placeholder - would integrate with AI)
        3. Convert response to audio
        
        Returns:
            Tuple of (transcribed_text, response_audio_file)
        """
        # Step 1: Transcribe
        transcribed = self.audio_to_text(audio_file)
        print(f"Transcribed: {transcribed}", file=sys.stderr)
        
        # Step 2: Generate response (placeholder - in real use, this would call the AI)
        response_text = f"I heard you say: {transcribed}. This is a test response from the voice system using Edge TTS."
        
        # Step 3: Convert to audio
        response_audio = self.text_to_audio(response_text)
        
        return transcribed, response_audio

if __name__ == "__main__":
    # Test the voice handler
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <audio_file>", file=sys.stderr)
        sys.exit(1)
    
    handler = VoiceHandler()
    transcribed, response_audio = handler.process_voice_message(sys.argv[1])
    
    print(f"Transcription: {transcribed}")
    if response_audio:
        print(f"Response audio: {response_audio}")
    else:
        print("Failed to generate response audio")