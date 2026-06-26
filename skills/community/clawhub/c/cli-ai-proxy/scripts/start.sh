#!/usr/bin/env bash
set -euo pipefail

# Start the cli-ai-proxy server.
# Usage: start.sh [-p port] [-h host]

if ! command -v cli-ai-proxy >/dev/null 2>&1; then
  echo "ERROR: cli-ai-proxy not found on PATH."
  echo "Run the install script first: {baseDir}/scripts/install.sh"
  exit 1
fi

exec cli-ai-proxy start "$@"
