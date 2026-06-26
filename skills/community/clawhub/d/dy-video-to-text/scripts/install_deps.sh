#!/usr/bin/env bash
# SECURITY MANIFEST:
#   Environment variables accessed: none
#   External endpoints called: https://pypi.org (pip install)
#   Local files read: none
#   Local files written: pip packages into site-packages or user site-packages

set -euo pipefail

echo "Installing douyin-video-processor dependencies..."

if command -v uv &> /dev/null; then
    uv pip install --system requests dashscope 2>/dev/null \
      || uv pip install requests dashscope
elif command -v pip3 &> /dev/null; then
    pip3 install --user requests dashscope 2>/dev/null \
      || pip3 install --break-system-packages requests dashscope 2>/dev/null \
      || pip3 install requests dashscope
elif command -v pip &> /dev/null; then
    pip install --user requests dashscope 2>/dev/null \
      || pip install --break-system-packages requests dashscope 2>/dev/null \
      || pip install requests dashscope
else
    echo "ERROR: No pip or uv found. Please install Python 3.10+ with pip."
    exit 1
fi

echo "Dependencies installed successfully."
