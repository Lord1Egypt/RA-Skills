#!/bin/bash
# patch-plist.sh — Re-adds critical keys to the OpenClaw gateway plist
# after openclaw overwrites it with `gateway start`.
# Triggered by launchd WatchPaths on the plist file.

PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
LOG="$HOME/.openclaw/logs/plist-patcher.log"
CHANGED=0

[ ! -f "$PLIST" ] && exit 0

# ExitTimeOut: force-kill after 10s if shutdown hangs
if ! plutil -p "$PLIST" 2>/dev/null | grep -q '"ExitTimeOut"'; then
    plutil -insert ExitTimeOut -integer 10 "$PLIST" 2>/dev/null && CHANGED=1
fi

# ProcessType: Interactive prevents launchd from delaying restarts
if ! plutil -p "$PLIST" 2>/dev/null | grep -q '"ProcessType"'; then
    plutil -insert ProcessType -string "Interactive" "$PLIST" 2>/dev/null && CHANGED=1
fi

# LowPriorityBackgroundIO: prevent IO throttling
if ! plutil -p "$PLIST" 2>/dev/null | grep -q '"LowPriorityBackgroundIO"'; then
    plutil -insert LowPriorityBackgroundIO -bool false "$PLIST" 2>/dev/null && CHANGED=1
fi

if [ "$CHANGED" -eq 1 ]; then
    echo "$(date '+%Y-%m-%dT%H:%M:%S%z') [plist-patcher] Patched gateway plist (ExitTimeOut+ProcessType+LowPriorityIO)" >> "$LOG"
fi
