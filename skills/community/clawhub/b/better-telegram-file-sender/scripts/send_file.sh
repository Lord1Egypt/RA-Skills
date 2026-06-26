#!/bin/bash
# Telegram File Sender Script
path="$1"
caption="${2:-File from OpenClaw}"
target="${3}"  # e.g., telegram:1234567890 — read from Inbound Context chat_id

if [ ! -f "$path" ]; then
  echo "File not found: $path"
  exit 1
fi

if [ -z "$target" ]; then
  echo "No target specified. Pass chat_id from Inbound Context as 3rd arg (e.g., telegram:1234567890)"
  exit 1
fi

echo "Sending $path to $target..."
openclaw message send --channel telegram --target "$target" --media "$path" --message "$caption"

echo "Sent!"
