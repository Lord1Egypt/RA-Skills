#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="link"
TARGET_DIR="${HOME}/.openclaw/workspace/skills/durable-task-runner"

usage() {
  cat <<EOF
Install durable-task-runner as an OpenClaw workspace skill.

Usage:
  $0 [--copy|--link] [--target DIR]

Defaults:
  --link
  --target ~/.openclaw/workspace/skills/durable-task-runner

Examples:
  $0
  $0 --copy
  $0 --target ~/.openclaw/workspace/skills/durable-task-runner
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)
      MODE="copy"
      shift
      ;;
    --link)
      MODE="link"
      shift
      ;;
    --target)
      TARGET_DIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown arg: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

mkdir -p "$(dirname "$TARGET_DIR")"

if [[ -e "$TARGET_DIR" || -L "$TARGET_DIR" ]]; then
  rm -rf "$TARGET_DIR"
fi

if [[ "$MODE" == "link" ]]; then
  ln -s "$ROOT" "$TARGET_DIR"
else
  mkdir -p "$TARGET_DIR"
  rsync -a \
    --exclude '.git/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude 'state/tasks/*.json' \
    --exclude 'state/tasks/*.jsonl' \
    --exclude 'state/tasks/*.log' \
    "$ROOT/" "$TARGET_DIR/"
fi

echo "Installed durable-task-runner -> $TARGET_DIR ($MODE)"
echo "Verify with: openclaw skills list | grep durable-task-runner"
