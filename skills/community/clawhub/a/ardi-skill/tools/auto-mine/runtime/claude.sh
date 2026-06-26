#!/usr/bin/env bash
# runtime/claude.sh — invoke Claude Code with the ardi mining tick prompt.
#
# Used by ardi-tick.sh when ARDI_AGENT_RUNTIME=claude (the default).
#
# Requires:
#   - claude binary on PATH (https://github.com/anthropics/claude-code)
#   - either ANTHROPIC_API_KEY in env, or `claude` already authed via OAuth
#
# Stdin: nothing.
# Stdout/stderr: passed through to journald via systemd.
# Exit: claude's exit code.

set -euo pipefail

PROMPT_FILE="${1:?usage: claude.sh <prompt-file>}"
[[ -r "$PROMPT_FILE" ]] || { echo "prompt not readable: $PROMPT_FILE" >&2; exit 2; }

command -v claude >/dev/null || { echo "claude not on PATH" >&2; exit 3; }

# --print: non-interactive one-shot
# --max-turns 30: hard cap on tool-use turns so a stuck loop can't burn
#   tokens forever (a healthy tick uses ~10 turns)
# Stream output so journald shows progress in real time.
exec claude \
  --print \
  --max-turns 30 \
  --output-format stream-json \
  --verbose \
  < "$PROMPT_FILE"
