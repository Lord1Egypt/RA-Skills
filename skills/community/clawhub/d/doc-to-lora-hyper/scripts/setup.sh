#!/usr/bin/env bash
# Setup Doc-to-LoRA on macOS (Apple Silicon).
# Installs Python dependencies (via uv pip install) and downloads model weights.
#
# This script does NOT download or execute any remote scripts.
# All installations use uv pip with pinned package versions.
#
# Prerequisites (install these yourself first):
#   - Python 3.10+: https://www.python.org/downloads/
#   - uv package manager: https://docs.astral.sh/uv/getting-started/installation/
#   - HF_TOKEN env var: https://huggingface.co/settings/tokens (with Gemma access)
#   - This script must run inside a doc-to-lora repo clone containing install_mac.sh
set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$REPO_ROOT"

echo "=== Doc-to-LoRA Setup (macOS) ==="
echo "Repo root: $REPO_ROOT"

# 1. Check all prerequisites
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is not installed."
    echo "Install it: https://www.python.org/downloads/"
    exit 1
fi

if ! command -v uv &>/dev/null; then
    echo "ERROR: uv is not installed."
    echo "Install it: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi
echo "[1/4] Prerequisites found: python3 $(python3 --version 2>&1 | cut -d' ' -f2), uv $(uv --version 2>&1)"

if [ -z "$HF_TOKEN" ]; then
    echo "ERROR: HF_TOKEN is not set."
    echo "Gemma 2 2B is a gated model requiring a HuggingFace access token."
    echo "1. Get a token at: https://huggingface.co/settings/tokens"
    echo "2. Accept Gemma license at: https://huggingface.co/google/gemma-2-2b-it"
    echo "3. Run: export HF_TOKEN=hf_your_token_here"
    exit 1
fi

if [ ! -f "install_mac.sh" ]; then
    echo "ERROR: install_mac.sh not found in $REPO_ROOT"
    echo "This skill must be used inside a doc-to-lora repository clone."
    echo "Clone it: git clone https://github.com/Manojbhat09/doc-to-lora-hyper-skill"
    exit 1
fi

# 2. Install Python dependencies (via install_mac.sh which uses uv pip install)
if [ ! -d ".venv" ]; then
    echo "[2/4] Installing Python dependencies (Mac-compatible, via uv pip install)..."
    bash install_mac.sh
else
    echo "[2/4] .venv already exists, skipping dependency install."
fi

# Activate
source .venv/bin/activate

# 3. Install MLX dependencies for fast Apple Silicon inference
echo "[3/4] Installing MLX dependencies (via uv pip install)..."
uv pip install mlx mlx-lm safetensors 2>/dev/null || true

# 4. Download pretrained D2L weights from HuggingFace
# Uses huggingface-cli which verifies checksums automatically.
# Source: https://huggingface.co/SakanaAI/doc-to-lora (official Sakana AI repo)
if [ ! -d "trained_d2l" ]; then
    echo "[4/4] Downloading Doc-to-LoRA weights from SakanaAI/doc-to-lora (~3GB)..."
    uv run huggingface-cli download SakanaAI/doc-to-lora --local-dir trained_d2l
else
    echo "[4/4] trained_d2l/ already present, skipping download."
fi

echo ""
echo "=== Setup complete ==="
echo "Activate:  source .venv/bin/activate"
echo ""
echo "Quick test:"
echo "  python demo_dario.py"
