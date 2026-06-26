#!/usr/bin/env bash
set -euo pipefail

# Usage:
# ./scripts/run-copilot-example.sh /path/to/repo "Implement X and add tests"

PROJECT_DIR="${1:-}"
TASK="${2:-}"

if [[ -z "$PROJECT_DIR" || -z "$TASK" ]]; then
  echo "Usage: $0 <project_dir> <task>"
  exit 1
fi

if ! command -v copilot >/dev/null 2>&1; then
  echo "Error: copilot not found. Install with: npm install -g @github/copilot"
  exit 1
fi

cd "$PROJECT_DIR"
copilot -p "$TASK" --allow-all-tools
