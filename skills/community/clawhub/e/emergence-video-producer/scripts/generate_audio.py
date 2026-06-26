import os
import subprocess
import argparse
from dotenv import load_dotenv

load_dotenv()

def generate_edge_tts(text, output_file, voice="zh-CN-XiaoxiaoNeural"):
    """Uses Edge-TTS (free, high quality)."""
    print(f"Generating Edge-TTS for: {text[:20]}...")
    cmd = [
        "edge-tts",
        "--text", text,
        "--write-media", output_file,
        "--voice", voice
    ]
    subprocess.run(cmd, check=True)
    print(f"✓ Audio saved to {output_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--output", default="narration.mp3")
    parser.add_argument("--voice", default="zh-CN-XiaoxiaoNeural")
    args = parser.parse_args()
    
    generate_edge_tts(args.text, args.output, args.voice)

if __name__ == "__main__":
    main()
