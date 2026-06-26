#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw" / "workspace"))
PIPER_DIR = WORKSPACE / "piper"
VENV_PY = SCRIPT_DIR / ".venv" / "bin" / "python"

REQUIRED_VOICES = [
    "pt_BR-jeff-medium.onnx",
    "pt_BR-cadu-medium.onnx",
    "pt_BR-faber-medium.onnx",
    "pt_BR-miro-high.onnx",
]


def check(name: str, ok: bool, details: str = "") -> bool:
    prefix = "✅" if ok else "❌"
    print(f"{prefix} {name}")
    if details:
        print(f"   {details}")
    return ok


def main() -> int:
    print("Audio PT Auto-Reply - Health Check")
    print("=" * 50)

    ok_all = True

    ok_all &= check("python3", shutil.which("python3") is not None, "Required OS dependency")
    ok_all &= check("ffmpeg", shutil.which("ffmpeg") is not None, "Required OS dependency")
    ok_all &= check("tar", shutil.which("tar") is not None, "Required OS dependency")
    ok_all &= check("curl/wget", shutil.which("curl") is not None or shutil.which("wget") is not None, "Required OS dependency")

    ok_all &= check("virtualenv python", VENV_PY.exists(), str(VENV_PY))
    piper_bin = PIPER_DIR / "piper" / "piper"
    ok_all &= check("piper binary", piper_bin.exists() and os.access(piper_bin, os.X_OK), str(piper_bin))

    for voice in REQUIRED_VOICES:
      ok_all &= check(f"voice model: {voice}", (PIPER_DIR / voice).exists(), str(PIPER_DIR / voice))

    cfg_path = WORKSPACE / ".audio_pt_voice_config.json"
    ok_all &= check("voice config", cfg_path.exists(), str(cfg_path))

    if VENV_PY.exists():
        try:
            result = subprocess.run(
                [str(VENV_PY), "-c", "import torch, torchaudio, transformers; print('ok')"],
                check=True,
                capture_output=True,
                text=True,
                timeout=20,
            )
            ok_all &= check("python dependencies", result.stdout.strip() == "ok", "torch, torchaudio, transformers")
        except Exception as exc:
            ok_all &= check("python dependencies", False, str(exc))

        try:
            result = subprocess.run(
                [str(VENV_PY), str(SCRIPT_DIR / "scripts" / "voice_config.py"), "get"],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            ok_all &= check("voice_config.py", bool(result.stdout.strip()), result.stdout.strip())
        except Exception as exc:
            ok_all &= check("voice_config.py", False, str(exc))

    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            result = subprocess.run(
                [str(VENV_PY), "-c", "import anthropic; print('ok')"],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            ok_all &= check("anthropic optional dependency", result.stdout.strip() == "ok", "ANTHROPIC_API_KEY is set")
        except Exception as exc:
            ok_all &= check("anthropic optional dependency", False, f"Set but package missing: {exc}")
    else:
        check("anthropic optional dependency", True, "Not configured; local mode will be used")

    print("=" * 50)
    print("Ready" if ok_all else "One or more checks failed")
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
