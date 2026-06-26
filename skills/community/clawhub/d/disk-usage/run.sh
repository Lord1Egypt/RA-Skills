#!/bin/bash
# disk-usage: Show disk space usage of a directory
# Arguments: [DIRECTORY] (optional, defaults to current directory; 1 arg max)
# Usage: bash run.sh [DIRECTORY]

set -euo pipefail

if [ $# -gt 1 ]; then
  echo "ERROR: Expected at most 1 argument: [DIRECTORY]"
  echo "Usage: bash run.sh [DIRECTORY]"
  exit 1
fi

DIR_PATH="${1:-.}"

if [ ! -d "$DIR_PATH" ]; then
  echo "ERROR: Directory not found: $DIR_PATH"
  exit 1
fi

du -sh "$DIR_PATH"/* 2>/dev/null | sort -rh | head -20
echo "---"
du -sh "$DIR_PATH"
