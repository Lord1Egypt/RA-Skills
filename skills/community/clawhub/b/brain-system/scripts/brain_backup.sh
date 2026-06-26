#!/usr/bin/env bash
set -euo pipefail
out_dir=/root/.openclaw/workspace/skills/brain-system/backups
mkdir -p "$out_dir"
ts=$(date +%Y-%m-%d-%H%M%S)
out="$out_dir/openclaw-brain-backup-$ts.tar.gz"
tar -czf "$out" -C /root/.openclaw/workspace \
  AGENTS.md SOUL.md USER.md TOOLS.md MEMORY.md memory skills/brain-system skills/server-body-ops context-checkpoints 2>/tmp/brain-backup-warn.log || true
if [ ! -s "$out" ]; then
  tar -czf "$out" -C /root/.openclaw/workspace memory skills/brain-system skills/server-body-ops context-checkpoints
fi
echo "$out"
