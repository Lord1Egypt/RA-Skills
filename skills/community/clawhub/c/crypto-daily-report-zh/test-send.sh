#!/bin/bash
# Test send crypto report to channel
# Usage: ./test-send.sh [CHANNEL_ID]

set -e

CHANNEL_ID="${1:--1002009088194}"

echo "Testing crypto daily report send to channel: $CHANNEL_ID"
echo ""
echo "This will generate a test report and send it to the specified channel."
echo ""

# The actual send would be done via the message tool
# This script serves as documentation

cat <<EOF
To test send a report, use the OpenClaw agent with:

message send \\
  --channel telegram \\
  --target "$CHANNEL_ID" \\
  --text "📰 币圈日报\\n..."

Or simply ask the agent: "Run crypto daily report and send to $CHANNEL_ID"
EOF
