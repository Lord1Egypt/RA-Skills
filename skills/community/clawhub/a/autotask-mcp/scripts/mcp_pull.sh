#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Pulling Autotask MCP image…"
docker compose pull
