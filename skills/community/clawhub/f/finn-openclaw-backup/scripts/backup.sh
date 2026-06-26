#!/bin/bash
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="$HOME/Desktop/OpenClawBackup-$DATE"

mkdir -p "$BACKUP_DIR"
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/"
cp -r ~/.openclaw/agents "$BACKUP_DIR/"
cp -r ~/.openclaw/credentials "$BACKUP_DIR/"
cp -r ~/.openclaw/cron "$BACKUP_DIR/"

echo "Backup created: $BACKUP_DIR"
