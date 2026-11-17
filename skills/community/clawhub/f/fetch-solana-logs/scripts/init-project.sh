#!/usr/bin/env bash
# Scaffold fetch-solana-logs Node.js project from skill templates.
# Usage: init-project.sh [target_directory]
set -euo pipefail

TARGET_DIR="${1:-fetch_solana_logs}"
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
mkdir -p "$TARGET_DIR/output"

# Ensure empty target list placeholder
if [ ! -f "$TARGET_DIR/target_solana_addr.json" ]; then
  printf '%s\n' '[]' > "$TARGET_DIR/target_solana_addr.json"
fi

if [ -n "${HELIUS_API_KEY:-}" ]; then
  {
    printf 'HELIUS_API_KEY=%s\n' "$HELIUS_API_KEY"
    if [ -n "${SOLANA_RPC_URL:-}" ]; then
      printf 'SOLANA_RPC_URL=%s\n' "$SOLANA_RPC_URL"
    fi
  } > "$TARGET_DIR/.env"
elif [ ! -f "$TARGET_DIR/.env" ] && [ -f "$TARGET_DIR/.env.example" ]; then
  cp "$TARGET_DIR/.env.example" "$TARGET_DIR/.env"
fi

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
echo "  1. Ask user for Solana address(es); write target_solana_addr.json"
echo "  2. Set HELIUS_API_KEY in .env (recommended)"
echo "  3. pnpm s1 -- --limit 50   then   pnpm s2"
echo "  4. If no on-chain IDL for a program, ask user for IDL JSON → output/<addr>/idl_<addr>.json"
