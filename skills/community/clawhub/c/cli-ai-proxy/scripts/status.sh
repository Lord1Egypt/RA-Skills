#!/usr/bin/env bash
set -euo pipefail

# Show cli-ai-proxy status and health information.

if ! command -v cli-ai-proxy >/dev/null 2>&1; then
  echo "Status: not installed"
  echo "Install with: {baseDir}/scripts/install.sh"
  exit 0
fi

exec cli-ai-proxy status
