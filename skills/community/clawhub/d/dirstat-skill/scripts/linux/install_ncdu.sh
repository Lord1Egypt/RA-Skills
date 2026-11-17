#!/usr/bin/env bash
set -euo pipefail

if command -v ncdu >/dev/null 2>&1; then
  echo "ncdu already installed"
  exit 0
fi

if sudo -n true >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y ncdu
  exit 0
fi

if [ -t 0 ]; then
  echo "ERROR: sudo password required; installation must be performed with operator input" >&2
  exit 4
fi

IFS= read -r SUDO_PASSWORD
if [ -z "$SUDO_PASSWORD" ]; then
  echo "ERROR: empty sudo password on stdin" >&2
  exit 5
fi

printf '%s\n' "$SUDO_PASSWORD" | sudo -S -p '' apt-get update
printf '%s\n' "$SUDO_PASSWORD" | sudo -S -p '' apt-get install -y ncdu
