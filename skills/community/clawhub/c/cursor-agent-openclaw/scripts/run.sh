#!/bin/bash
# cursor-agent/scripts/run.sh
#
# Usage: run.sh <repo_path> <task> [model] [mode]
#
# model: sonnet-4.6 (default) | opus-4.6-thinking | auto
# mode:  ask    — read-only, no file changes (DEFAULT)
#        plan   — planning only, no file changes
#        write  — applies changes (--force); requires explicit user approval before calling
#
# IMPORTANT: Default mode is 'ask' (read-only). Only pass mode=write after the user
# has explicitly confirmed they want changes applied to the repo.

REPO="${1:?repo path required}"
TASK="${2:?task required}"
MODEL="${3:-sonnet-4.6}"
MODE="${4:-ask}"

# Verify agent CLI is available
if ! command -v agent &>/dev/null; then
  echo "ERROR: 'agent' CLI not found. Install from: https://cursor.com/docs/cli/overview" >&2
  exit 1
fi

cd "$REPO" || exit 1

case "$MODE" in
  write)
    # Destructive — applies changes to files. Only call after explicit user consent.
    ARGS=(-p "$TASK" --force --output-format text --trust)
    ;;
  plan)
    # Read-only planning mode
    ARGS=(-p "$TASK" --mode=plan --output-format text --trust)
    ;;
  ask|*)
    # Default: read-only exploration, no file changes
    ARGS=(-p "$TASK" --mode=ask --output-format text --trust)
    ;;
esac

if [ "$MODEL" != "auto" ]; then
  ARGS+=(--model "$MODEL")
fi

agent "${ARGS[@]}"
