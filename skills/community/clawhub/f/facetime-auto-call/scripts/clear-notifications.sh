#!/usr/bin/env bash
# Clear Notification Center notifications

set -euo pipefail

echo "=== Clearing Notification Center ==="
killall NotificationCenter 2>/dev/null || true
sleep 2
sleep 2

RESULT=$(osascript <<'CHECK'
tell application "System Events"
    tell process "NotificationCenter"
        if exists window "Notification Center" then
            tell window "Notification Center"
                try
                    set allGroups to every group of scroll area 1 of group 1 of group 1
                    return count of allGroups
                on error
                    return -1
                end try
            end tell
        else
            return 0
        end if
    end tell
end tell
CHECK
)

if [ "$RESULT" = "0" ]; then
    echo "✅ Notifications cleared"
elif [ "$RESULT" = "-1" ]; then
    echo "⚠️ Unable to verify notification status"
else
    echo "⚠️ $RESULT notifications remain"
fi

echo "=== Done ==="
