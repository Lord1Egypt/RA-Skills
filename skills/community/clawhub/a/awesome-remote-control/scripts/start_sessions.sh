#!/usr/bin/env bash
# Start N Claude Code remote control sessions in parallel.
# Usage: start_sessions.sh <working-dir> <count> [--resume [uuid]]
#
# Example: start_sessions.sh /path/to/project 3

WORKDIR="${1:?Usage: start_sessions.sh <working-dir> <count> [--resume [uuid]]}"
COUNT="${2:-3}"
shift 2 2>/dev/null || true
EXTRA_ARGS=("$@")  # pass through --resume, etc.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validate count is a positive integer (#3)
if ! [[ "$COUNT" =~ ^[1-9][0-9]*$ ]]; then
  echo "Error: count must be a positive integer, got '$COUNT'" >&2
  exit 1
fi

# Reject --resume with multiple sessions — all N would fight over the same UUID
for arg in "${EXTRA_ARGS[@]}"; do
  if [[ "$arg" == "--resume" && "$COUNT" -gt 1 ]]; then
    echo "Error: --resume cannot be used with count > 1 (all sessions would resume the same UUID)." >&2
    exit 1
  fi
done

echo "🚀 Starting $COUNT sessions in parallel for: $WORKDIR"
echo ""

OUTDIR=$(mktemp -d)
PIDS=()

for i in $(seq 1 "$COUNT"); do
  OUTFILE="$OUTDIR/session_$i.txt"
  bash "$SCRIPT_DIR/start_session.sh" "$WORKDIR" "${EXTRA_ARGS[@]}" > "$OUTFILE" 2>&1 &
  PIDS+=($!)
done

# Wait for all to complete, tracking failures (#25)
FAILURES=0
for pid in "${PIDS[@]}"; do
  wait "$pid" || ((FAILURES++))
done

# Print all outputs in order
for i in $(seq 1 "$COUNT"); do
  cat "$OUTDIR/session_$i.txt"
  echo ""
done

# Print summary of session URLs in easy-to-copy format
echo "────────────────────────────────────────"
echo "Session URLs:"
grep -rh 'URL:' "$OUTDIR"/ 2>/dev/null | sed 's/.*URL: */  /' | grep -v '<not captured'
echo "────────────────────────────────────────"

rm -rf "$OUTDIR"

if [[ $FAILURES -gt 0 ]]; then
  echo "⚠️  $FAILURES of $COUNT sessions failed to start." >&2
  exit 1
fi
