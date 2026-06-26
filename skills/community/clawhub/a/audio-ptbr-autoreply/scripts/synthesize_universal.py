#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw" / "workspace"))
PIPER_DIR = WORKSPACE / "piper"
DEFAULT_TIMEOUT = int(os.environ.get("SYNTHESIS_TIMEOUT", "45"))

VOICE_MAP = {
    "jeff": "pt_BR-jeff-medium.onnx",
    "cadu": "pt_BR-cadu-medium.onnx",
    "faber": "pt_BR-faber-medium.onnx",
    "miro": "pt_BR-miro-high.onnx",
    "feminina": "pt_BR-miro-high.onnx",
    "masculina": "pt_BR-jeff-medium.onnx",
}


class SynthesisError(Exception):
    pass


def read_text(args: argparse.Namespace) -> str:
    if args.stdin:
        return sys.stdin.read().strip()
    if args.input_file:
        return Path(args.input_file).read_text(encoding="utf-8").strip()
    if args.text is not None:
        return args.text.strip()
    raise SynthesisError("No text provided")


def get_paths(voice: str) -> tuple[Path, Path]:
    model = VOICE_MAP.get(voice.lower(), VOICE_MAP["jeff"])
    piper_bin = PIPER_DIR / "piper" / "piper"
    model_path = PIPER_DIR / model

    if not piper_bin.exists():
        raise SynthesisError(f"Piper binary not found: {piper_bin}")
    if not os.access(piper_bin, os.X_OK):
        raise SynthesisError(f"Piper binary is not executable: {piper_bin}")
    if not model_path.exists():
        raise SynthesisError(f"Voice model not found: {model_path}")

    return piper_bin, model_path


def synthesize_to_file(text: str, voice: str = "jeff", timeout: int = DEFAULT_TIMEOUT) -> Path:
    if not text.strip():
        raise SynthesisError("Text cannot be empty")

    piper_bin, model_path = get_paths(voice)
    out_dir = Path(tempfile.gettempdir())
    wav_path = out_dir / "audio_pt_reply.wav"
    ogg_path = out_dir / "audio_pt_reply.ogg"

    for path in (wav_path, ogg_path):
        if path.exists():
            path.unlink()

    try:
        subprocess.run(
            [str(piper_bin), "--model", str(model_path), "--output_file", str(wav_path)],
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=timeout,
            check=True,
        )
    except subprocess.TimeoutExpired as exc:
        raise SynthesisError(f"Piper timed out after {timeout}s") from exc
    except subprocess.CalledProcessError as exc:
        raise SynthesisError(exc.stderr.decode("utf-8", errors="ignore")) from exc

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(wav_path),
                "-c:a",
                "libopus",
                "-b:a",
                "32k",
                str(ogg_path),
            ],
            capture_output=True,
            timeout=timeout,
            check=True,
        )
    except subprocess.TimeoutExpired as exc:
        raise SynthesisError(f"ffmpeg timed out after {timeout}s") from exc
    except subprocess.CalledProcessError as exc:
        raise SynthesisError(exc.stderr.decode("utf-8", errors="ignore")) from exc
    finally:
        if wav_path.exists():
            wav_path.unlink()

    if not ogg_path.exists():
        raise SynthesisError("OGG output was not created")
    return ogg_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="?")
    parser.add_argument("--stdin", action="store_true", help="Read text from stdin")
    parser.add_argument("--input-file", help="Read text from a UTF-8 file")
    parser.add_argument("--voice", default=os.environ.get("AUDIO_VOICE", "jeff"))
    parser.add_argument("--print-path", action="store_true", help="Print output file path only")
    args = parser.parse_args()

    try:
        text = read_text(args)
        path = synthesize_to_file(text, args.voice)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
