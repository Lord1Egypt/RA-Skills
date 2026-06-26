#!/usr/bin/env python3
"""
flow_voice.py — One-shot voice cloning + speech generation via LuxTTS.

Usage:
  # Clone and speak immediately
  python flow_voice.py --sample ref.wav --text "Hello world" --output out.wav

  # Use saved profile
  python flow_voice.py --voice eric --text "Hello world" --output out.wav

  # Save profile for reuse
  python flow_voice.py --sample ref.wav --name eric --text "Hello" --output out.wav

  # Bake voiceover into video
  python flow_voice.py --sample ref.wav --text "Your agent draws now." \
    --video animation.mp4 --output final.mp4
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "zipvoice",
#   "soundfile",
#   "librosa",
#   "numpy",
# ]
# ///

import argparse
import os
import pickle
import subprocess
import sys
import tempfile
from pathlib import Path

PROFILES_DIR = Path.home() / "clawd/output/voice/profiles"
OUTPUT_DIR = Path.home() / "clawd/output/voice"


def detect_device() -> str:
    """Auto-detect best available device."""
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"


def load_model(device: str):
    """Load LuxTTS model."""
    print(f"  🔧 Loading LuxTTS on {device}...")
    from zipvoice.luxvoice import LuxTTS
    lux = LuxTTS("YatharthS/LuxTTS", device=device)
    print("  ✅ Model loaded")
    return lux


def encode_voice(lux, sample_path: str, duration: int = 1000) -> object:
    """Encode a voice reference sample."""
    print(f"  🎤 Encoding voice from: {sample_path}")
    encoded = lux.encode_prompt(sample_path, duration=duration, rms=0.01)
    print("  ✅ Voice encoded")
    return encoded


def save_profile(encoded, name: str) -> Path:
    """Save an encoded voice profile."""
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    path = PROFILES_DIR / f"{name}.pkl"
    with open(path, "wb") as f:
        pickle.dump(encoded, f)
    print(f"  💾 Profile saved: {path}")
    return path


def load_profile(name: str) -> object:
    """Load a saved voice profile."""
    path = PROFILES_DIR / f"{name}.pkl"
    if not path.exists():
        print(f"  ❌ No profile found for '{name}' at {path}", file=sys.stderr)
        print(f"  💡 Clone a voice first: --sample ref.wav --name {name}", file=sys.stderr)
        sys.exit(1)
    with open(path, "rb") as f:
        encoded = pickle.load(f)
    print(f"  ✅ Profile loaded: {name}")
    return encoded


def generate_speech(
    lux,
    text: str,
    encoded,
    output_path: Path,
    steps: int = 4,
    t_shift: float = 0.9,
    speed: float = 1.0,
    smooth: bool = False,
) -> Path:
    """Generate speech from text using encoded voice."""
    import soundfile as sf
    import numpy as np

    print(f"  🗣️  Generating speech: '{text[:60]}{'...' if len(text) > 60 else ''}'")
    wav = lux.generate_speech(
        text,
        encoded,
        num_steps=steps,
        t_shift=t_shift,
        speed=speed,
        return_smooth=smooth,
    )
    wav_np = wav.numpy().squeeze()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output_path), wav_np, 48000)
    print(f"  ✅ Audio saved: {output_path}")
    return output_path


def bake_into_video(audio_path: Path, video_path: str, output_path: Path) -> Path:
    """Bake voiceover audio into a video using ffmpeg."""
    print(f"  🎬 Baking audio into video: {video_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(output_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ❌ ffmpeg error: {result.stderr[-300:]}", file=sys.stderr)
        sys.exit(1)
    print(f"  ✅ Video with voice saved: {output_path}")
    return output_path


def list_profiles():
    """List all saved voice profiles."""
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    profiles = list(PROFILES_DIR.glob("*.pkl"))
    if not profiles:
        print("No saved voice profiles. Use --sample + --name to create one.")
    else:
        print(f"Saved voice profiles ({len(profiles)}):")
        for p in sorted(profiles):
            size_kb = p.stat().st_size // 1024
            print(f"  • {p.stem} ({size_kb}KB) — use with --voice {p.stem}")


def main():
    parser = argparse.ArgumentParser(
        description="FlowVoice — Clone any voice with LuxTTS"
    )
    parser.add_argument("--sample", help="Reference audio file (wav/mp3, min 3s)")
    parser.add_argument("--voice", help="Use saved voice profile by name")
    parser.add_argument("--name", help="Save cloned profile with this name")
    parser.add_argument("--text", help="Text to speak")
    parser.add_argument("--output", help="Output file path (.wav or .mp4 if --video)")
    parser.add_argument("--video", help="Bake voiceover into this video file")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (default: 1.0)")
    parser.add_argument("--steps", type=int, default=4, help="Inference steps (default: 4)")
    parser.add_argument("--t-shift", type=float, default=0.9, help="Sampling param (default: 0.9)")
    parser.add_argument("--smooth", action="store_true", help="Enable smoothing (reduces metallic artifacts)")
    parser.add_argument("--device", help="Device: cpu / mps / cuda (default: auto)")
    parser.add_argument("--list", action="store_true", help="List saved voice profiles")
    args = parser.parse_args()

    if args.list:
        list_profiles()
        return

    if not args.text:
        parser.error("--text is required")
    if not args.sample and not args.voice:
        parser.error("Either --sample or --voice is required")

    device = args.device or detect_device()
    print(f"\n🎙️  FlowVoice — LuxTTS")
    print(f"   Device: {device}")

    lux = load_model(device)

    # Get encoded voice
    if args.voice:
        encoded = load_profile(args.voice)
    else:
        encoded = encode_voice(lux, args.sample)
        if args.name:
            save_profile(encoded, args.name)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        from datetime import datetime
        ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        ext = "mp4" if args.video else "wav"
        output_path = OUTPUT_DIR / f"{ts}-flowvoice.{ext}"

    # Generate speech
    if args.video:
        # Need a temp wav first, then bake into video
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_wav = Path(tmp.name)
        generate_speech(lux, args.text, encoded, tmp_wav, args.steps, args.t_shift, args.speed, args.smooth)
        bake_into_video(tmp_wav, args.video, output_path)
        tmp_wav.unlink(missing_ok=True)
    else:
        generate_speech(lux, args.text, encoded, output_path, args.steps, args.t_shift, args.speed, args.smooth)

    print(f"\n✨ Done! Output: {output_path}")


if __name__ == "__main__":
    main()
