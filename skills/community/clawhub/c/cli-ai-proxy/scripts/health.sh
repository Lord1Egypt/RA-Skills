#!/usr/bin/env bash
set -euo pipefail

# Health check — outputs JSON from the /health endpoint.
# Exit code 0 if healthy, 1 if unreachable.

if ! command -v cli-ai-proxy >/dev/null 2>&1; then
  echo '{"status":"not_installed","error":"cli-ai-proxy not found on PATH"}'
  exit 1
fi

exec cli-ai-proxy health
