#!/usr/bin/env bash
# Install dependencies for the Essay Humanizer skill (Apple Silicon only).
# Usage: bash scripts/install_deps.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Installing MLX + inference deps (requires Apple Silicon macOS)..."
pip install --upgrade mlx mlx-lm transformers

echo "Decoding LoRA adapter (one-time, from base64 JSON)..."
python3 "$SCRIPT_DIR/decode_adapters.py"

echo "Done. The base model (Qwen3-8B-MLX-4bit) downloads from HuggingFace on first run."
