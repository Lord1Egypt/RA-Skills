#!/usr/bin/env bash
set -euo pipefail

if [ -z "${BF16_API_KEY:-}" ]; then
  echo "Error: export BF16_API_KEY='sk-bf16-v1-...' first." >&2
  exit 1
fi

echo "[bf16] Verifying API key against https://api.bf16.ai/v1/models..."
curl -fsS https://api.bf16.ai/v1/models \
  -H "Authorization: Bearer $BF16_API_KEY" >/dev/null
echo "[bf16] Key verified."

if command -v openclaw >/dev/null 2>&1; then
  openclaw config set provider.openai.baseUrl "https://api.bf16.ai/v1"
  openclaw config set provider.openai.apiKey "$BF16_API_KEY"
  openclaw config set model.default "deepseek/deepseek-v4.1-flash-uncensored-fast"
  echo "[bf16] OpenClaw configured for bf16.ai (deepseek/deepseek-v4.1-flash-uncensored-fast)."
else
  echo "[bf16] openclaw CLI not found in PATH. Use these settings in your OpenClaw config:"
  echo "  Base URL: https://api.bf16.ai/v1"
  echo "  Model:    deepseek/deepseek-v4.1-flash-uncensored-fast"
fi
