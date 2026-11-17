#!/usr/bin/env bash
set -euo pipefail

if ! command -v ncdu >/dev/null 2>&1; then
  echo "ERROR: ncdu not found in PATH" >&2
  exit 127
fi

echo "ncdu_path=$(command -v ncdu)"
ncdu --version
