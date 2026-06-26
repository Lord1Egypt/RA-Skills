#!/bin/bash
# check-memory.sh — Check available physical RAM before spawning a new agent
# Usage: check-memory.sh
# Stdout: FREE_MB=N  STATUS=ok|warn|block  REASON=...
# Exit:   0=ok  1=warn(low but still allow)  2=block(too low, refuse)
#
# Thresholds (tuned for 16GB Mac Mini + swap, running up to 4 Codex + 2 CC):
#   Each Codex     ≈ 200-400MB
#   Each CC        ≈ 400-800MB
#   4 Codex + 2CC  ≈ 2GB agents total, leaving ample headroom on 16GB
#
#   > 4096MB free → ok,    spawn freely
#   2048-4096MB   → warn,  spawn but notify
#   < 2048MB      → block, entering swap territory, refuse

set -euo pipefail

OK_THRESHOLD=4096    # MB — comfortable
BLOCK_THRESHOLD=2048 # MB — absolute minimum (below = swap risk)

# macOS vm_stat: free + inactive pages are immediately reclaimable
PAGE_SIZE=$(vm_stat | awk '/page size of/{print $8}')
FREE_PAGES=$(vm_stat | awk '/Pages free:/{gsub(/\./,"",$3); print $3}')
INACTIVE_PAGES=$(vm_stat | awk '/Pages inactive:/{gsub(/\./,"",$3); print $3}')

FREE_MB=$(( (FREE_PAGES + INACTIVE_PAGES) * PAGE_SIZE / 1048576 ))

echo "FREE_MB=$FREE_MB"

if [[ $FREE_MB -lt $BLOCK_THRESHOLD ]]; then
  echo "STATUS=block"
  echo "REASON=Only ${FREE_MB}MB free RAM (min: ${BLOCK_THRESHOLD}MB). System may already be using swap."
  exit 2
elif [[ $FREE_MB -lt $OK_THRESHOLD ]]; then
  echo "STATUS=warn"
  echo "REASON=${FREE_MB}MB free RAM (comfortable: ${OK_THRESHOLD}MB). Spawning with caution."
  exit 1
else
  echo "STATUS=ok"
  echo "REASON=${FREE_MB}MB free RAM — plenty of headroom."
  exit 0
fi
