#!/usr/bin/env python3
"""Universal Transcribe - Works in both OpenClaw and Claude environments."""
import sys
import json
import os
from pathlib import Path
from typing import Optional, Dict

try:
    from transformers import pipeline
except ImportError:
    raise ImportError("transformers not installed. Run: pip install transformers torch torchaudio")


class PortugueseTranscriber:
    """Portuguese Brazilian transcriber using wav2vec2."""
    
    _pipeline = None
    
    @classmethod
    def get_pipeline(cls):
        """Get or create the transcription pipeline."""
        if cls._pipeline is None:
            print("Loading transcription model (first run may take a moment)...", file=sys.stderr)
            cls._pipeline = pipeline(
                "automatic-speech-recognition",
                model="jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
            )
        return cls._pipeline
    
    @classmethod
    def transcribe(cls, audio_path: str, language: str = "pt") -> Dict:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file (WAV, OGG, MP3, etc)
            language: Language code (pt for Portuguese, en for English)
        
        Returns:
            Dictionary with 'text' key containing transcription
        """
        
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Get pipeline
        pipe = cls.get_pipeline()
        
        # Transcribe
        result = pipe(str(audio_path))
        
        return {
            "text": result.get("text", "").strip(),
            "language": language,
            "model": "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese",
            "success": True
        }


def transcribe_file(audio_path: str) -> str:
    """
    Transcribe audio file and return text.
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        Transcribed text
    """
    result = PortugueseTranscriber.transcribe(audio_path)
    return result["text"]


def transcribe_file_json(audio_path: str) -> Dict:
    """
    Transcribe audio file and return JSON result.
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        Dictionary with transcription result
    """
    return PortugueseTranscriber.transcribe(audio_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No audio file"}), file=sys.stderr)
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    try:
        result = transcribe_file_json(audio_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Transcription failed: {str(e)}"}), file=sys.stderr)
        sys.exit(1)
