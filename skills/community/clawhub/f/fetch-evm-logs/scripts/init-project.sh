#!/usr/bin/env bash
# Scaffold fetch-evm-logs Node.js project from skill templates.
# Usage: init-project.sh [target_directory]
set -euo pipefail

TARGET_DIR="${1:-fetch_evm_logs}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_DIR="$SKILL_DIR/templates"

if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "templates/ not found at $TEMPLATE_DIR"
  exit 1
fi

if [ -e "$TARGET_DIR" ]; then
  if [ -n "$(ls -A "$TARGET_DIR" 2>/dev/null)" ]; then
    echo "Target $TARGET_DIR exists and is not empty. Choose another path or remove it."
    exit 1
  fi
else
  mkdir -p "$TARGET_DIR"
fi

cp -R "$TEMPLATE_DIR/." "$TARGET_DIR/"
mkdir -p "$TARGET_DIR/output" "$TARGET_DIR/src/abi"

echo "Scaffolded at $(cd "$TARGET_DIR" && pwd)"
echo "Installing dependencies..."

if command -v pnpm >/dev/null 2>&1; then
  (cd "$TARGET_DIR" && pnpm install)
elif command -v npm >/dev/null 2>&1; then
  (cd "$TARGET_DIR" && npm install)
else
  echo "No pnpm/npm found. Run install manually in $TARGET_DIR"
  exit 1
fi

echo ""
echo "Done. Next steps:"
echo "  1. Ask user for chainId + contractAddress"
echo "  2. Try fetch-abi.mjs; if that fails, ask user to provide ABI JSON"
echo "  3. List events, ask which to pull"
echo "  4. Edit src/contract.ts, then: pnpm s1 && pnpm s2"
