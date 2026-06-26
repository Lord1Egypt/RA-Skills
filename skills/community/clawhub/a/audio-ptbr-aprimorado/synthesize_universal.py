#!/usr/bin/env python3
"""Universal Synthesize - Production-grade TTS with proper error handling."""
import sys
import os
import subprocess
import json
import logging
import tempfile
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'WARNING'),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get timeout from environment (default 30s)
DEFAULT_TIMEOUT = int(os.environ.get('SYNTHESIS_TIMEOUT', '30'))

class SynthesisError(Exception):
    """Base exception for synthesis errors."""
    pass

class ModelNotFoundError(SynthesisError):
    """Piper model not found."""
    pass

class PiperError(SynthesisError):
    """Piper TTS error."""
    pass

class ConversionError(SynthesisError):
    """FFmpeg conversion error."""
    pass

class PortugueseVoiceSynthesizer:
    """Portuguese Brazilian TTS using Piper with proper error handling."""
    
    # Voice mapping
    VOICES = {
        'jeff': 'pt_BR-jeff-medium.onnx',
        'cadu': 'pt_BR-cadu-medium.onnx',
        'faber': 'pt_BR-faber-medium.onnx',
        'miro': 'pt_BR-miro-high.onnx',
        'feminina': 'pt_BR-miro-high.onnx',
        'masculina': 'pt_BR-jeff-medium.onnx',
    }
    
    def __init__(self, piper_dir: Optional[Path] = None):
        """
        Initialize synthesizer.
        
        Args:
            piper_dir: Path to Piper directory (auto-detected if None)
        """
        if piper_dir:
            self.piper_dir = Path(piper_dir)
        else:
            self.piper_dir = self._find_piper_dir()
        
        self.piper_binary = self.piper_dir / "piper" / "piper"
        
        # Validate setup
        self._validate_setup()
    
    @staticmethod
    def _find_piper_dir() -> Path:
        """Find Piper directory (searches common locations)."""
        candidates = [
            Path.home() / ".openclaw/workspace/piper",
            Path.home() / ".claude-audio-pt/piper",
            Path.home() / ".audio-pt-autoreply/piper",
            Path("/opt/piper"),
            Path("/usr/local/piper"),
        ]
        
        for path in candidates:
            if (path / "piper" / "piper").exists():
                logger.debug(f"Found Piper at: {path}")
                return path
        
        raise ModelNotFoundError(
            f"Piper not found in common locations. Searched: {', '.join(str(p) for p in candidates)}"
        )
    
    def _validate_setup(self):
        """Validate Piper installation."""
        if not self.piper_binary.exists():
            raise ModelNotFoundError(f"Piper binary not found at {self.piper_binary}")
        
        if not self.piper_binary.is_file():
            raise ModelNotFoundError(f"Piper is not a file: {self.piper_binary}")
        
        if not os.access(self.piper_binary, os.X_OK):
            raise ModelNotFoundError(f"Piper is not executable: {self.piper_binary}")
        
        logger.debug(f"Piper validated: {self.piper_binary}")
    
    def _get_model_path(self, voice: str) -> Path:
        """Get full path to voice model."""
        model_name = self.VOICES.get(voice.lower(), self.VOICES['jeff'])
        model_path = self.piper_dir / model_name
        
        if not model_path.exists():
            raise ModelNotFoundError(
                f"Voice model not found: {model_path}\n"
                f"Available voices: {', '.join(self.VOICES.keys())}"
            )
        
        return model_path
    
    def synthesize_to_file(
        self,
        text: str,
        voice: str = 'jeff',
        output_path: Optional[Path] = None,
        timeout: int = DEFAULT_TIMEOUT
    ) -> Path:
        """
        Synthesize text to OGG audio file.
        
        Args:
            text: Text to synthesize
            voice: Voice name (jeff, cadu, faber, miro, feminina, masculina)
            output_path: Output file path (created if None)
            timeout: Process timeout in seconds
            
        Returns:
            Path to output OGG file
            
        Raises:
            SynthesisError: On any synthesis failure
        """
        
        # Validate input
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Get voice model
        model_path = self._get_model_path(voice)
        logger.debug(f"Using voice model: {model_path.name}")
        
        # Set output path
        if output_path is None:
            tmpdir = Path(os.environ.get('TMPDIR', '/tmp'))
            output_path = tmpdir / 'autoreply_out.ogg'
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Temporary WAV file
        temp_wav = output_path.parent / f"{output_path.stem}_temp.wav"
        
        try:
            # Stage 1: Piper TTS (WAV)
            logger.info(f"Synthesizing with Piper ({len(text)} chars)...")
            
            try:
                subprocess.run(
                    [str(self.piper_binary), "--model", str(model_path), "--output_file", str(temp_wav)],
                    input=text.encode('utf-8'),
                    check=True,
                    capture_output=True,
                    timeout=timeout
                )
            except subprocess.TimeoutExpired:
                raise PiperError(f"Piper timed out after {timeout}s")
            except subprocess.CalledProcessError as e:
                raise PiperError(
                    f"Piper failed: {e.stderr.decode('utf-8', errors='replace') if e.stderr else 'unknown error'}"
                )
            except FileNotFoundError:
                raise PiperError("Piper binary not executable")
            
            if not temp_wav.exists() or temp_wav.stat().st_size == 0:
                raise PiperError("Piper produced no output")
            
            logger.debug(f"WAV created: {temp_wav.stat().st_size} bytes")
            
            # Stage 2: FFmpeg conversion (WAV → OGG)
            logger.info("Converting to OGG/Opus...")
            
            try:
                subprocess.run(
                    [
                        "ffmpeg",
                        "-i", str(temp_wav),
                        "-c:a", "libopus",
                        "-b:a", "32k",
                        "-y",  # Overwrite
                        str(output_path)
                    ],
                    capture_output=True,
                    check=True,
                    timeout=timeout
                )
            except subprocess.TimeoutExpired:
                raise ConversionError(f"FFmpeg timed out after {timeout}s")
            except subprocess.CalledProcessError as e:
                raise ConversionError(
                    f"FFmpeg failed: {e.stderr.decode('utf-8', errors='replace') if e.stderr else 'unknown error'}"
                )
            except FileNotFoundError:
                raise ConversionError("FFmpeg not found in PATH. Install with: apt-get install ffmpeg")
            
            if not output_path.exists() or output_path.stat().st_size == 0:
                raise ConversionError("FFmpeg produced no output")
            
            logger.info(f"Synthesis complete: {output_path.stat().st_size} bytes")
            
            return output_path
            
        finally:
            # Cleanup temporary WAV
            temp_wav.unlink(missing_ok=True)
    
    def synthesize_to_bytes(
        self,
        text: str,
        voice: str = 'jeff',
        timeout: int = DEFAULT_TIMEOUT
    ) -> bytes:
        """
        Synthesize text to audio bytes (OGG format).
        
        Args:
            text: Text to synthesize
            voice: Voice name
            timeout: Process timeout
            
        Returns:
            Audio bytes in OGG/Opus format
        """
        with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as f:
            temp_path = f.name
        
        try:
            output_path = self.synthesize_to_file(text, voice, Path(temp_path), timeout)
            
            with open(output_path, 'rb') as f:
                audio_bytes = f.read()
            
            return audio_bytes
            
        finally:
            Path(temp_path).unlink(missing_ok=True)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: synthesize_universal.py 'text' [voice]", file=sys.stderr)
        print("Voices: jeff, cadu, faber, miro, feminina, masculina", file=sys.stderr)
        sys.exit(1)
    
    text = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('AUDIO_VOICE', 'jeff')
    
    try:
        synthesizer = PortugueseVoiceSynthesizer()
        output_path = synthesizer.synthesize_to_file(text, voice)
        print(str(output_path))
        sys.exit(0)
        
    except ModelNotFoundError as e:
        logger.error(f"Setup error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
        
    except (PiperError, ConversionError) as e:
        logger.error(f"Synthesis error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(4)


if __name__ == "__main__":
    main()
