#!/usr/bin/env python3
"""
Fun-ASR-Nano-2512 Single File Transcription Script
Wrapper for FunAsrTranscriber.py
"""

import argparse
import os
import sys
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from FunAsrTranscriber import AsrTranscriber
except ImportError as e:
    print(f"Error: Cannot import FunAsrTranscriber: {e}")
    print("Please ensure funasr is installed: pip install funasr modelscope")
    sys.exit(1)


def transcribe_file(audio_path, output_path=None, device="cpu"):
    """Transcribe a single audio file"""
    
    audio_path = Path(audio_path)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)
    
    # Default output path
    if output_path is None:
        output_path = audio_path.with_suffix('.txt')
    else:
        output_path = Path(output_path)
    
    print(f"Loading Fun-ASR-Nano-2512 model (device: {device})...")
    
    # Change to scripts directory for model loading
    original_cwd = os.getcwd()
    os.chdir(script_dir)
    
    try:
        # Modify device setting by environment variable
        import FunAsrTranscriber
        
        # Initialize transcriber
        transcriber = AsrTranscriber()
        
        print(f"Transcribing: {audio_path}")
        
        # Transcribe
        result = transcriber.transcribe_sync(str(audio_path))
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"✓ Transcription saved to: {output_path}")
        print(f"  Preview: {result[:100]}...")
        
        return output_path
        
    except Exception as e:
        print(f"Error during transcription: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        os.chdir(original_cwd)


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe audio using Fun-ASR-Nano-2512'
    )
    parser.add_argument('audio_file', help='Path to audio file')
    parser.add_argument('-o', '--output', help='Output text file path')
    parser.add_argument('-d', '--device', default='cpu',
                        choices=['cpu', 'cuda:0'],
                        help='Device to use (default: cpu)')
    
    args = parser.parse_args()
    
    # Set device via environment variable (if supported by your implementation)
    os.environ['FUNASR_DEVICE'] = args.device
    
    transcribe_file(
        audio_path=args.audio_file,
        output_path=args.output,
        device=args.device
    )


if __name__ == '__main__':
    main()
