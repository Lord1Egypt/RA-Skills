#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

AGENT_NAME="Andri"
BASE_DIR="$HOME/.openclaw/workspace/skills/meeting-room"
TO_LEADER="$BASE_DIR/to_leader.txt"

# Pastikan file ada
touch "$TO_LEADER"

while true; do
  ts=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$ts] $AGENT_NAME : sedang idle" >> "$TO_LEADER"
  sleep 30   # kirim status tiap 30 detik (ubah bila perlu)
done
