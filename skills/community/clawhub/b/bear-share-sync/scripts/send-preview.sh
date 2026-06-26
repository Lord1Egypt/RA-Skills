#!/usr/bin/env bash
# send-preview.sh — Send a note preview via BlueBubbles iMessage
# Usage: send-preview.sh <target> <title> <summary>
set -euo pipefail

TARGET="$1"
TITLE="$2"
SUMMARY="$3"

# Truncate summary to 280 chars
SUMMARY=$(echo "$SUMMARY" | head -c 280)

MSG="📝 New shared note: ${TITLE}

${SUMMARY}…

🔗 See canvas for full node."

# This script is a helper — the actual send must go through the OpenClaw message tool.
# When invoked by the agent, the agent should call:
#   message(action="send", channel="bluebubbles", target=TARGET, message=MSG)
# This script outputs the formatted message for the agent to relay.

echo "$MSG"
