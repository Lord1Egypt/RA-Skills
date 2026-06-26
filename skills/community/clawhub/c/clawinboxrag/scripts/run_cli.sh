#!/usr/bin/env bash
set -euo pipefail

# Community wrapper for running gmail-rag CLI commands safely.
# Usage examples:
#   run_cli.sh status
#   run_cli.sh search "spot on" --hybrid --limit 5

GMAIL_RAG_REPO="${GMAIL_RAG_REPO:-}"
GMAIL_RAG_UV_BIN="${GMAIL_RAG_UV_BIN:-uv}"

if [[ -z "$GMAIL_RAG_REPO" ]]; then
  echo "ERROR: GMAIL_RAG_REPO is not set" >&2
  exit 2
fi

if [[ ! -d "$GMAIL_RAG_REPO" ]]; then
  echo "ERROR: GMAIL_RAG_REPO does not exist: $GMAIL_RAG_REPO" >&2
  exit 2
fi

if [[ $# -lt 1 ]]; then
  echo "ERROR: missing gmail-rag CLI subcommand" >&2
  exit 2
fi

if ! command -v "$GMAIL_RAG_UV_BIN" >/dev/null 2>&1; then
  echo "ERROR: runner not found in PATH: $GMAIL_RAG_UV_BIN" >&2
  exit 2
fi

subcommand="$1"
case "$subcommand" in
  search|recents|status|labels|ingest-primary|embed|refresh-labels)
    ;;
  *)
    echo "ERROR: subcommand not allowed by community skill policy: $subcommand" >&2
    exit 2
    ;;
esac

cd "$GMAIL_RAG_REPO"
exec "$GMAIL_RAG_UV_BIN" run python -m gmail_rag.cli "$@"
