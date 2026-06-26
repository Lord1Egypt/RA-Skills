#!/usr/bin/env python3
"""
Fun-ASR-Nano-2512 Batch Transcription Script
Wrapper for FunAsrTranscriber.py
"""

import argparse
import os
import sys
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

# Add scripts directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))


def transcribe_single(args):
    """Worker function for parallel transcription"""
    audio_file, output_dir, device = args
    
    try:
        from FunAsrTranscriber import AsrTranscriber
        
        # Change to scripts directory
        original_cwd = os.getcwd()
        os.chdir(script_dir)
        
        try:
            # Initialize transcriber (each process loads its own model)
            transcriber = AsrTranscriber()
            
            audio_path = Path(audio_file)
            output_path = output_dir / audio_path.with_suffix('.txt').name
            
            # Transcribe
            result = transcriber.transcribe_sync(str(audio_path))
            
            # Write output
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            
            return (audio_file, True, str(output_path))
        finally:
            os.chdir(original_cwd)
            
    except Exception as e:
        import traceback
        return (audio_file, False, str(e))


def batch_transcribe(input_dir, output_dir=None, device='cpu', jobs=1):
    """Batch transcribe all audio files in a directory"""
    
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"Error: Directory not found: {input_path}")
        sys.exit(1)
    
    # Supported audio formats
    audio_extensions = {'.wav', '.mp3', '.m4a', '.aac', '.ogg', '.flac'}
    
    # Find all audio files
    audio_files = [
        f for f in input_path.iterdir()
        if f.is_file() and f.suffix.lower() in audio_extensions
    ]
    
    if not audio_files:
        print(f"No audio files found in {input_path}")
        print(f"Supported formats: {', '.join(audio_extensions)}")
        sys.exit(1)
    
    print(f"Found {len(audio_files)} audio files")
    
    # Create output directory
    if output_dir is None:
        output_dir = input_path.parent / f"{input_path.name}_transcripts"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Prepare arguments
    tasks = [(str(f), output_dir, device) for f in audio_files]
    
    # Process files
    start_time = time.time()
    success_count = 0
    failed_count = 0
    
    if jobs > 1:
        print(f"Processing with {jobs} parallel jobs (device: {device})...")
        print("Note: Each job will load its own model instance")
        
        with ProcessPoolExecutor(max_workers=jobs) as executor:
            futures = {executor.submit(transcribe_single, task): task[0] for task in tasks}
            
            for future in as_completed(futures):
                audio_file, success, message = future.result()
                if success:
                    print(f"✓ {Path(audio_file).name}")
                    success_count += 1
                else:
                    print(f"✗ {Path(audio_file).name}: {message}")
                    failed_count += 1
    else:
        print(f"Processing sequentially (device: {device})...")
        
        # Import here to avoid loading model in main process
        from FunAsrTranscriber import AsrTranscriber
        
        # Change to scripts directory
        original_cwd = os.getcwd()
        os.chdir(script_dir)
        
        try:
            print("Loading Fun-ASR-Nano-2512 model...")
            transcriber = AsrTranscriber()
            
            for i, audio_file in enumerate(audio_files, 1):
                audio_path = Path(audio_file)
                output_file = output_dir / audio_path.with_suffix('.txt').name
                
                print(f"[{i}/{len(audio_files)}] {audio_path.name}")
                
                try:
                    result = transcriber.transcribe_sync(str(audio_path))
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result)
                    
                    success_count += 1
                except Exception as e:
                    print(f"  Error: {e}")
                    failed_count += 1
        finally:
            os.chdir(original_cwd)
    
    elapsed = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"Batch transcription complete!")
    print(f"  Total files: {len(audio_files)}")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Time: {elapsed:.1f}s")
    if len(audio_files) > 0:
        print(f"  Avg: {elapsed/len(audio_files):.1f}s per file")
    print(f"  Output: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description='Batch transcribe audio files using Fun-ASR-Nano-2512'
    )
    parser.add_argument('directory', help='Directory containing audio files')
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument('-d', '--device', default='cpu',
                        choices=['cpu', 'cuda:0'],
                        help='Device to use (default: cpu)')
    parser.add_argument('-j', '--jobs', type=int, default=1,
                        help='Number of parallel jobs (default: 1)')
    
    args = parser.parse_args()
    
    # Set device via environment variable
    os.environ['FUNASR_DEVICE'] = args.device
    
    batch_transcribe(
        input_dir=args.directory,
        output_dir=args.output,
        device=args.device,
        jobs=args.jobs
    )


if __name__ == '__main__':
    main()
