#!/usr/bin/env bash
set -euo pipefail

# Packaging-agnostic runtime:
# - ANNAS_MCP_COMMAND: executable name or absolute path (default: annas-mcp)
# - ANNAS_MCP_SOURCE_DIR: optional source dir to auto-build binary into /tmp

BIN_CANDIDATE="${ANNAS_MCP_COMMAND:-annas-mcp}"
SOURCE_DIR="${ANNAS_MCP_SOURCE_DIR:-}"
BUILD_BIN_PATH="${ANNAS_BUILD_BIN_PATH:-/tmp/annas-mcp-hardened}"

if [ -n "$SOURCE_DIR" ]; then
  if [ ! -d "$SOURCE_DIR" ]; then
    echo "ANNAS_MCP_SOURCE_DIR does not exist: $SOURCE_DIR" >&2
    exit 1
  fi

  needs_build=0
  if [ ! -x "$BUILD_BIN_PATH" ]; then
    needs_build=1
  elif find "$SOURCE_DIR" -type f \( -name '*.go' -o -name 'go.mod' -o -name 'go.sum' \) -newer "$BUILD_BIN_PATH" | head -n1 | grep -q .; then
    needs_build=1
  fi

  if [ "$needs_build" -eq 1 ]; then
    (cd "$SOURCE_DIR" && go build -o "$BUILD_BIN_PATH" ./cmd/annas-mcp)
  fi

  BIN_CANDIDATE="$BUILD_BIN_PATH"
fi

if [[ "$BIN_CANDIDATE" == */* ]]; then
  BIN_PATH="$BIN_CANDIDATE"
  if [ ! -x "$BIN_PATH" ]; then
    echo "Anna MCP binary is not executable: $BIN_PATH" >&2
    exit 1
  fi
else
  BIN_PATH="$(command -v "$BIN_CANDIDATE" || true)"
  if [ -z "$BIN_PATH" ]; then
    echo "Anna MCP command not found: $BIN_CANDIDATE" >&2
    echo "Set ANNAS_MCP_COMMAND or ANNAS_MCP_SOURCE_DIR before running." >&2
    exit 1
  fi
fi

export ANNAS_BASE_URL="${ANNAS_BASE_URL:-annas-archive.gl}"
export ANNAS_ALLOWED_HOSTS="${ANNAS_ALLOWED_HOSTS:-annas-archive.gl,annas-archive.vg,annas-archive.pk,annas-archive.gd,annas-archive.li,annas-archive.pm,annas-archive.in,annas-archive.org}"
export ANNAS_DOWNLOAD_PATH="${ANNAS_DOWNLOAD_PATH:-/tmp/annas-archive-downloads}"
export ANNAS_HTTP_TIMEOUT_SECONDS="${ANNAS_HTTP_TIMEOUT_SECONDS:-30}"
export ANNAS_MAX_DOWNLOAD_SIZE_BYTES="${ANNAS_MAX_DOWNLOAD_SIZE_BYTES:-120000000}"

mkdir -p "$ANNAS_DOWNLOAD_PATH"

# The CLI warns when .env is missing in cwd.
if [ ! -f /tmp/.env ]; then
  : > /tmp/.env
fi
cd /tmp

exec "$BIN_PATH" "$@"
