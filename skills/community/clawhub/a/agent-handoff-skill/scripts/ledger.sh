#!/bin/sh
# Print the relay ledger for one task, oldest hop first.
# Match the parsed Task-Id trailer literally, never a commit-body mention.
# Usage: ledger.sh <task-id>
set -eu

TASK=${1:?usage: ledger.sh <task-id>}

LOG=$(git log --reverse \
  --format='%(trailers:key=Task-Id,valueonly,separator=%x1f,unfold=true)%x09%ad  hop=%(trailers:key=Hop,valueonly,separator=)  agent=%(trailers:key=Agent,valueonly,separator=)  %s' \
  --date=short)
OUT=$(printf '%s\n' "$LOG" | HANDOFF_LEDGER_TASK="$TASK" awk '
  BEGIN { FS = "\t" }
  $1 == ENVIRON["HANDOFF_LEDGER_TASK"] {
    sub(/^[^\t]*\t/, "")
    print
  }
')

if [ -z "$OUT" ]; then
  printf 'no commits found for task: %s\n' "$TASK" >&2
  exit 1
fi

printf '%s\n' "$OUT"
