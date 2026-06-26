#!/usr/bin/env bash

# Assumes social-auto-upload already cloned to $SAU_HOME and `uv sync --python 3.12` already ran.
SAU_HOME="$HOME/.openclaw/social-auto-upload"


set -euo pipefail

# account_name is user-defined. One account_name maps to one account file.
# You can prepare multiple account names and run them in parallel.
account="account_a"
video="videos/demo.mp4"
thumbnail="videos/demo.png"

uv run --project "$SAU_HOME" python sau_cli.py douyin login --account "$account" --headless
uv run --project "$SAU_HOME" python sau_cli.py douyin check --account "$account"

uv run --project "$SAU_HOME" python sau_cli.py douyin upload-video \
  --account "$account" \
  --file "$video" \
  --title "Douyin video from bash" \
  --desc "Douyin video description from bash" \
  --tags "cli,video" \
  --thumbnail "$thumbnail" \
  --headless

uv run --project "$SAU_HOME" python sau_cli.py douyin upload-note \
  --account "$account" \
  --images "videos/1.png" "videos/2.png" \
  --title "Douyin note title from bash" \
  --note "Douyin note from bash" \
  --tags "cli,note" \
  --headless
