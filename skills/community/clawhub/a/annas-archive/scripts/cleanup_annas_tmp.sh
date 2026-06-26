#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${ANNAS_DOWNLOAD_PATH:-/tmp/annas-archive-downloads}"
MAX_AGE_DAYS="${1:-7}"

if [ ! -d "$TARGET_DIR" ]; then
  exit 0
fi

find "$TARGET_DIR" -type f -mtime "+$MAX_AGE_DAYS" -delete
find "$TARGET_DIR" -type d -empty -delete
