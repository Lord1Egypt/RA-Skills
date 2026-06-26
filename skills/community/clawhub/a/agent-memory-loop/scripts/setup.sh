#!/usr/bin/env bash
# setup.sh — Initialize agent-memory-loop v2 in a workspace
# Usage: bash setup.sh [workspace_path]
#
# Wrapper for install.sh (kept for backward compatibility)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "${SCRIPT_DIR}/install.sh" "$@"
