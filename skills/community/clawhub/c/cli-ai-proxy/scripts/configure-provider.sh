#!/usr/bin/env bash
set -euo pipefail

# Configure OpenClaw to use cli-ai-proxy as a model provider.
# Adds the provider config to ~/.openclaw/openclaw.json and registers models.
# The underlying CLI writes a timestamped .bak file next to the config before modifying it.

if ! command -v cli-ai-proxy >/dev/null 2>&1; then
  echo "ERROR: cli-ai-proxy not found on PATH."
  echo "Run the install script first: {baseDir}/scripts/install.sh"
  exit 1
fi

exec cli-ai-proxy configure-openclaw "$@"
