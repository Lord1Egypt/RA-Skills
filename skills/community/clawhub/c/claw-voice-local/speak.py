#!/usr/bin/env python3
"""
speak.py — Text → OGG Opus audio via piper TTS.

Requires:
  - piper binary: ~/.local/bin/piper
  - voice model: ~/.local/share/piper/<model>.onnx
  - ffmpeg (for WAV → OGG conversion)

Usage:
  python3 speak.py --text "Hello world"
  python3 speak.py --text "Hello" --output /tmp/out.ogg
  python3 speak.py --text "Hello" --model ~/.local/share/piper/en_US-amy-low.onnx
  echo "Hello" | python3 speak.py
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PIPER_BIN   = Path.home() / ".local" / "bin" / "piper"
PIPER_LIBS  = Path.home() / ".local" / "lib" / "piper"
MODEL_DIR   = Path.home() / ".local" / "share" / "piper"
DEFAULT_OUTPUT = Path("/tmp/claw_voice_output.ogg")


def _find_default_model() -> Path | None:
    """Find any .onnx model in the model directory."""
    if not MODEL_DIR.exists():
        return None
    models = sorted(MODEL_DIR.glob("*.onnx"))
    return models[0] if models else None


def check_deps(model: Path) -> None:
    """Check that piper, the voice model, and ffmpeg are available."""
    errors = []
    if not PIPER_BIN.exists():
        errors.append(
            f"piper binary not found: {PIPER_BIN}\n"
            "  → See README.md for installation instructions."
        )
    if not model.exists():
        errors.append(
            f"Voice model not found: {model}\n"
            "  → Download a model from https://huggingface.co/rhasspy/piper-voices\n"
            "  → Place the .onnx and .onnx.json files in ~/.local/share/piper/"
        )
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        errors.append("ffmpeg not found — install via: sudo apt install ffmpeg")
    if errors:
        print("Dependency check failed:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)


def synthesize(
    text: str,
    output: Path,
    model: Path,
    length_scale: float | None = None,
) -> Path:
    """Convert text to OGG Opus via piper + ffmpeg."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = Path(tmp.name)

    try:
        # Set up environment for piper shared libraries
        env = os.environ.copy()
        existing = env.get("LD_LIBRARY_PATH", "")
        env["LD_LIBRARY_PATH"] = f"{PIPER_LIBS}:{existing}" if existing else str(PIPER_LIBS)
        espeak_data = MODEL_DIR / "espeak-ng-data"
        if espeak_data.exists():
            env["ESPEAK_DATA_PATH"] = str(espeak_data)

        # piper: text → WAV
        cmd = [str(PIPER_BIN), "--model", str(model), "--output_file", str(wav_path)]
        if length_scale is not None:
            cmd += ["--length-scale", str(length_scale)]

        subprocess.run(
            cmd,
            input=text.encode("utf-8"),
            capture_output=True,
            check=True,
            env=env,
        )

        # ffmpeg: WAV → OGG Opus (Telegram-compatible)
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(wav_path),
                "-c:a", "libopus",
                "-b:a", "32k",
                "-vbr", "on",
                str(output),
            ],
            capture_output=True,
            check=True,
        )

    finally:
        if wav_path.exists():
            wav_path.unlink()

    return output


def main():
    parser = argparse.ArgumentParser(description="Text → OGG Opus via piper TTS")
    parser.add_argument("--text", "-t", help="Text to speak (or use stdin)")
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUTPUT), help="Output .ogg file path")
    parser.add_argument("--model", "-m", help="Path to piper .onnx voice model")
    parser.add_argument(
        "--length-scale", "-s",
        type=float, default=None, dest="length_scale",
        help="Speed control: <1.0 = faster, >1.0 = slower (default: 1.0)"
    )
    args = parser.parse_args()

    # Resolve model path
    if args.model:
        model = Path(args.model)
    else:
        model = _find_default_model()
        if model is None:
            print(
                "ERROR: No voice model found in ~/.local/share/piper/\n"
                "  → Download a model from https://huggingface.co/rhasspy/piper-voices",
                file=sys.stderr
            )
            sys.exit(1)

    check_deps(model)

    # Read text
    if args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    else:
        parser.error("Provide --text or pipe text via stdin")

    if not text:
        print("ERROR: Empty text", file=sys.stderr)
        sys.exit(1)

    output = Path(args.output)
    result = synthesize(text, output, model, args.length_scale)
    print(str(result))


if __name__ == "__main__":
    main()
