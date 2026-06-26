#!/bin/bash
# feishu_backup.sh — Download files from a Feishu group chat and save to backup directory.
#
# Basic usage (download latest file):
#   ./feishu_backup.sh
#
# Smart-matching usage (agent sets env vars based on user intent):
#   LIMIT=2 ./feishu_backup.sh                           # latest 2 files
#   NAME_PREFIX=report ./feishu_backup.sh                # files starting with "report"
#   MINUTES=5 FILE_TYPE=pdf ./feishu_backup.sh           # PDFs from the last 5 minutes
#   MINUTES=5 FILE_TYPE=video ./feishu_backup.sh         # videos from the last 5 minutes
#   LIMIT=3 MINUTES=10 ./feishu_backup.sh                # up to 3 files from the last 10 minutes

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOWNLOADER="$SCRIPT_DIR/../shared/feishu_downloader.py"
BACKUP_DIR="${BACKUP_DIR:-$HOME/.openclaw/doc/backup}"

mkdir -p "$BACKUP_DIR"

source "$SCRIPT_DIR/../shared/feishu_args.sh"

python3 "$DOWNLOADER" "${FEISHU_ARGS[@]}" "$BACKUP_DIR"
