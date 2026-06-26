#!/usr/bin/env bash
# setup.sh — Install all doc-process skill dependencies
#
# Usage:
#   bash skills/doc-process/setup.sh          # install everything
#   bash skills/doc-process/setup.sh --light  # Python packages only (no system deps)
#
# Runs from your project root (the directory where skills/ lives).

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIGHT=false
[[ "${1:-}" == "--light" ]] && LIGHT=true

# ── Step 1: Ensure Python 3 is available ─────────────────────────────────────
echo "=== doc-process: checking Python ==="
if command -v python3 &>/dev/null; then
    echo "✓ $(python3 --version)"
    PY=python3
elif command -v python &>/dev/null && python -c "import sys; assert sys.version_info.major==3" 2>/dev/null; then
    echo "✓ $(python --version)"
    PY=python
else
    echo "✗ Python 3 not found. Install it first:"
    echo "    Amazon Linux / RHEL:  sudo yum install -y python3"
    echo "    Ubuntu / Debian:      sudo apt-get install -y python3"
    echo "    macOS:                brew install python"
    exit 1
fi

# ── Step 2: Ensure pip is available ──────────────────────────────────────────
echo ""
echo "=== doc-process: ensuring pip is installed ==="
if $PY -m pip --version &>/dev/null; then
    echo "✓ $($PY -m pip --version)"
else
    echo "  pip not found — installing via ensurepip..."
    if $PY -m ensurepip --upgrade 2>/dev/null; then
        echo "✓ pip installed via ensurepip"
    else
        echo "  ensurepip unavailable — trying package manager..."
        if command -v apt-get &>/dev/null; then
            sudo apt-get install -y python3-pip
        elif command -v yum &>/dev/null; then
            sudo yum install -y python3-pip
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y python3-pip
        elif command -v brew &>/dev/null; then
            brew install python   # pip is bundled with Homebrew Python
        else
            echo "  Falling back to get-pip.py..."
            curl -sSL https://bootstrap.pypa.io/get-pip.py | $PY
        fi
    fi
    # Upgrade pip to latest
    $PY -m pip install --upgrade pip --quiet
    echo "✓ $($PY -m pip --version)"
fi

# ── Step 3: Install Python packages ──────────────────────────────────────────
echo ""
echo "=== doc-process: installing Python dependencies ==="
$PY -m pip install -r "$SKILL_DIR/requirements.txt" --quiet && \
    echo "✓ Python packages installed" || \
    { echo "✗ pip install failed — try: $PY -m pip install --user -r skills/doc-process/requirements.txt"; exit 1; }

if $LIGHT; then
    echo "Skipping system packages (--light mode)."
    exit 0
fi

echo ""
echo "=== doc-process: checking system dependencies ==="

# ── tesseract (needed by redactor.py image mode) ─────────────────────────────
if command -v tesseract &>/dev/null; then
    echo "✓ tesseract $(tesseract --version 2>&1 | head -1 | awk '{print $2}')"
else
    echo "  tesseract not found — installing..."
    if command -v brew &>/dev/null; then
        brew install tesseract
    elif command -v apt-get &>/dev/null; then
        sudo apt-get install -y tesseract-ocr
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y tesseract
    else
        echo "  ⚠ Could not auto-install tesseract. Install manually:"
        echo "    macOS:  brew install tesseract"
        echo "    Ubuntu: apt install tesseract-ocr"
        echo "    (image redaction will not work without it)"
    fi
fi

# ── ffmpeg (needed by audio_transcriber.py) ──────────────────────────────────
if command -v ffmpeg &>/dev/null; then
    echo "✓ ffmpeg $(ffmpeg -version 2>&1 | head -1 | awk '{print $3}')"
else
    echo "  ffmpeg not found — installing..."
    if command -v brew &>/dev/null; then
        brew install ffmpeg
    elif command -v apt-get &>/dev/null; then
        sudo apt-get install -y ffmpeg
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y ffmpeg
    else
        echo "  ⚠ Could not auto-install ffmpeg. Install manually:"
        echo "    macOS:  brew install ffmpeg"
        echo "    Ubuntu: apt install ffmpeg"
        echo "    (audio transcription will not work without it)"
    fi
fi

echo ""
echo "=== doc-process: setup complete ==="
echo "All script-assisted modes are ready."
echo "Note: openai-whisper will download its model file (~140 MB) on first audio transcription."
