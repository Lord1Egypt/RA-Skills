#!/bin/bash
# Sync dev repo to OpenClaw runtime directory
set -e

SOURCE="/Users/leo/Documents/个人AI项目/Huper/amber-hunter"
TARGET="$HOME/.openclaw/skills/amber-hunter"

echo "Syncing amber-hunter dev → OpenClaw runtime..."
rsync -av \
  --exclude='.git' \
  --exclude='.synapse' \
  --exclude='.knowledge' \
  --exclude='memory.db' \
  --exclude='*.lance/' \
  --exclude='session_wal.jsonl' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.pytest_cache' \
  --exclude='.DS_Store' \
  "$SOURCE/" "$TARGET/"

echo "Done. Restart OpenClaw or reload amber-hunter skill to apply changes."
