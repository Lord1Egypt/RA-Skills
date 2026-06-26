#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
SKILL_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)

if [[ "${1:-}" != "help" && "${1:-}" != "--help" && -z "${E2B_API_KEY:-}" ]]; then
  echo "Missing E2B_API_KEY. Configure it in Vault / env before using this skill." >&2
  exit 1
fi

if [[ ! -d "$SKILL_DIR/node_modules/e2b" ]]; then
  echo "[e2b-sandbox] Installing Node dependencies in $SKILL_DIR ..." >&2
  (cd "$SKILL_DIR" && npm install --silent)
fi

exec node "$SCRIPT_DIR/e2b-sandbox.mjs" "$@"
