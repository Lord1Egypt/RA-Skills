#!/bin/bash
# websearch.sh - Free web search via Claude Code or Codex CLI WebSearch tool
# Usage: websearch.sh "query" [max_results] [--backend claude|codex]
#
# Requires: claude CLI (https://claude.ai/code) OR codex CLI (https://openai.com/codex)
# No API key needed beyond what's already configured for these CLIs.

QUERY=""
MAX_RESULTS=5
BACKEND=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --backend) BACKEND="$2"; shift 2 ;;
    --max) MAX_RESULTS="$2"; shift 2 ;;
    *) QUERY="${QUERY}${QUERY:+ }$1"; shift ;;
  esac
done

if [ -z "$QUERY" ]; then
  echo "Usage: websearch.sh \"query\" [--max N] [--backend claude|codex]" >&2
  exit 1
fi

PROMPT="Search the web for: ${QUERY}

Return a concise summary with up to ${MAX_RESULTS} key findings. Include source URLs."

# Auto-detect backend if not specified
if [ -z "$BACKEND" ]; then
  if command -v claude &>/dev/null; then
    BACKEND="claude"
  elif command -v codex &>/dev/null; then
    BACKEND="codex"
  else
    echo "Error: neither 'claude' nor 'codex' CLI found in PATH." >&2
    exit 1
  fi
fi

case "$BACKEND" in
  claude)
    claude -p "$PROMPT" --allowedTools "WebSearch" 2>/dev/null
    ;;
  codex)
    # Codex needs --skip-git-repo-check outside a git repo
    # Runs from /tmp to avoid workspace context loading delay
    TMPDIR_SEARCH=$(mktemp -d)
    cd "$TMPDIR_SEARCH"
    codex --search -c reasoning_effort=low exec --skip-git-repo-check "$PROMPT" 2>/dev/null
    cd - > /dev/null
    rm -rf "$TMPDIR_SEARCH"
    ;;
  *)
    echo "Unknown backend: $BACKEND. Use 'claude' or 'codex'." >&2
    exit 1
    ;;
esac
