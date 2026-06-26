#!/usr/bin/env bash
set -euo pipefail

# Stop the cli-ai-proxy server.

if ! command -v cli-ai-proxy >/dev/null 2>&1; then
  echo "ERROR: cli-ai-proxy not found on PATH."
  exit 1
fi

exec cli-ai-proxy stop
