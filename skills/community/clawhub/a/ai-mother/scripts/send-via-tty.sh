#!/bin/bash
# Send message to Claude via TTY (works when Claude is waiting for input)
# Usage: ./send-via-tty.sh <PID> <message>

PID=$1
MSG=$2

if [ -z "$PID" ] || [ -z "$MSG" ]; then
    echo "Usage: $0 <PID> <message>"
    exit 1
fi

# Get TTY
TTY=$(ps -o tty= -p "$PID" | xargs)
if [ "$TTY" = "?" ]; then
    echo "❌ Process has no TTY"
    exit 1
fi

TTY_DEV="/dev/$TTY"
if [ ! -w "$TTY_DEV" ]; then
    echo "❌ Cannot write to $TTY_DEV (permission denied)"
    exit 1
fi

echo "📤 Sending to TTY: $TTY_DEV"
echo "   Message: $MSG"

# Send message directly to TTY
printf '%s\n' "$MSG" > "$TTY_DEV" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Message sent to TTY"
else
    echo "❌ Failed to send (exit code: $EXIT_CODE)"
fi

exit $EXIT_CODE
