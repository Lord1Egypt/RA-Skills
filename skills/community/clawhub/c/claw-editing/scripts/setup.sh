#!/bin/bash
# Setup for the claw-editing skill (safe to re-run).
# - Creates a Python venv at ~/.cache/claw-editing/venv and installs from PyPI:
#   skia-python, pillow, numpy, and mlx-whisper (Apple Silicon) or faster-whisper (other CPUs).
# - Checks that ffmpeg/ffprobe are available (brew install ffmpeg, or set OPENCLAW_FFMPEG).
# The Whisper model (~1.6 GB) is downloaded from Hugging Face on first transcription.
set -e
V="$HOME/.cache/claw-editing/venv"
[ -x "$V/bin/python" ] || python3 -m venv "$V"
if [ "$(uname -s)-$(uname -m)" = "Darwin-arm64" ]; then ASR=mlx-whisper; ASRMOD=mlx_whisper; else ASR=faster-whisper; ASRMOD=faster_whisper; fi
"$V/bin/python" -c "import $ASRMOD, skia, PIL, numpy" 2>/dev/null || \
  "$V/bin/pip" -q install "$ASR" skia-python pillow numpy 2>&1 | grep -v -i "warning\|upgrade" || true
"$V/bin/python" -c "import $ASRMOD, skia, PIL, numpy; print('python ok: $V/bin/python ($ASR)')"
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE" && "$V/bin/python" -c "import render; print('ffmpeg ok:', render.FFMPEG)"
