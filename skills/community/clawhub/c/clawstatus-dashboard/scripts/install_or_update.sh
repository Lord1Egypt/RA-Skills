#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-$HOME/ClawStatus}"
REPO_URL="${REPO_URL:-https://github.com/NeverChenX/ClawStatus.git}"

if [[ -d "$TARGET_DIR/.git" ]]; then
  echo "[clawstatus] updating existing checkout: $TARGET_DIR"
  git -C "$TARGET_DIR" pull --ff-only
else
  echo "[clawstatus] cloning repo to: $TARGET_DIR"
  git clone "$REPO_URL" "$TARGET_DIR"
fi

echo "[clawstatus] installing editable package"
python3 -m pip install --user --break-system-packages -e "$TARGET_DIR"

echo "[clawstatus] done"
