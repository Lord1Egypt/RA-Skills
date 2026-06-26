#!/usr/bin/env bash
# stop.sh — pause auto-mine. Reversible via install.sh re-run or
# `systemctl --user start ardi-mine.timer`.
set -euo pipefail
systemctl --user stop ardi-mine.timer 2>/dev/null || true
echo "auto-mine paused. To resume: systemctl --user start ardi-mine.timer"
