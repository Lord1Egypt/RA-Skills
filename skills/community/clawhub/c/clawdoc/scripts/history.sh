#!/usr/bin/env bash
set -euo pipefail

VERSION="0.12.0"

# history.sh <sessions-directory>
# Cross-session recurrence tracker. Runs diagnose on all sessions,
# tracks Pattern-Key recurrence. Outputs promotion suggestions when
# threshold met (3+ occurrences across 2+ sessions in 30 days).
# Output is JSON.

usage() {
  cat <<EOF
Usage: history.sh [--help|--version] <sessions-directory>

Description:
  Cross-session recurrence tracker. Outputs pattern recurrence and promotion suggestions.

Options:
  --help      Show this help message and exit
  --version   Show version and exit

Example:
  history.sh ~/.openclaw/agents/main/sessions/ | jq .
EOF
}

check_deps() {
  for dep in jq awk; do
    if ! command -v "$dep" >/dev/null 2>&1; then
      echo "Error: required dependency '$dep' not found. Install it and retry." >&2
      exit 1
    fi
  done
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIAGNOSE="$SCRIPT_DIR/diagnose.sh"

if [ $# -ge 1 ]; then
  case "$1" in
    --help) usage; exit 0 ;;
    --version) echo "$VERSION"; exit 0 ;;
  esac
fi

check_deps

if [ $# -lt 1 ]; then
  echo "Usage: history.sh <sessions-directory>" >&2
  exit 1
fi

SESSIONS_DIR="$1"

if [ ! -d "$SESSIONS_DIR" ]; then
  echo "Error: directory not found: $SESSIONS_DIR" >&2
  exit 1
fi

# Collect all JSONL files
SESSION_FILES=()
while IFS= read -r -d '' f; do
  SESSION_FILES+=("$f")
done < <(find "$SESSIONS_DIR" -name "*.jsonl" -print0 2>/dev/null || true)

if [ ${#SESSION_FILES[@]} -eq 0 ]; then
  echo '{"sessions_analyzed":0,"pattern_recurrence":{},"promotion_suggestions":[]}'
  exit 0
fi

echo "[history] analyzing ${#SESSION_FILES[@]} session(s)..." >&2

# Collect per-session findings
RECURRENCE_FILE=$(mktemp /tmp/clawdoc_history.XXXXXX)
trap 'rm -f "$RECURRENCE_FILE"' EXIT

SESSIONS_ANALYZED=0
SESSION_IDS_BY_PATTERN_FILE=$(mktemp /tmp/clawdoc_sessions.XXXXXX)
trap 'rm -f "$RECURRENCE_FILE" "$SESSION_IDS_BY_PATTERN_FILE"' EXIT

for f in "${SESSION_FILES[@]}"; do
  sess_id=$(jq -r 'select(.type=="session") | .sessionId // "unknown"' "$f" 2>/dev/null | head -1)
  sess_ts=$(jq -r 'select(.type=="session") | .timestamp // ""' "$f" 2>/dev/null | head -1)

  findings=$(bash "$DIAGNOSE" "$f" 2>/dev/null || echo "[]")
  count=$(echo "$findings" | jq 'length')

  if [ "$count" -gt 0 ]; then
    echo "$findings" | jq -r --arg sid "$sess_id" --arg ts "$sess_ts" \
      '.[] | [$sid, $ts, .pattern, (.pattern_id | tostring), .severity, (.cost_impact // 0 | tostring)] | @tsv' \
      >> "$RECURRENCE_FILE"
  fi

  SESSIONS_ANALYZED=$((SESSIONS_ANALYZED + 1))
done

# Aggregate recurrence data
if [ ! -s "$RECURRENCE_FILE" ]; then
  echo "{\"sessions_analyzed\":$SESSIONS_ANALYZED,\"pattern_recurrence\":{},\"promotion_suggestions\":[]}"
  exit 0
fi

# Build recurrence summary using awk
# Format: session_id TAB timestamp TAB pattern TAB pattern_id TAB severity TAB cost_impact
RECURRENCE_JSON=$(awk -F'\t' '
{
  pattern = $3
  pattern_id = $4
  severity = $5
  cost = $6 + 0
  sess = $1
  ts = $2

  # Count occurrences per pattern
  counts[pattern]++
  total_cost[pattern] += cost

  # Track unique sessions per pattern
  key = pattern SUBSEP sess
  if (!seen[key]) {
    seen[key] = 1
    session_counts[pattern]++
    sessions_list[pattern] = sessions_list[pattern] " " sess
  }

  # Track severity
  if (!(pattern in severity_map)) {
    severity_map[pattern] = severity
    pattern_id_map[pattern] = pattern_id
  }
}
END {
  printf "{"
  first = 1
  for (p in counts) {
    if (!first) printf ","
    first = 0
    gsub(/"/, "\\\"", p)
    printf "\"%s\":{\"occurrences\":%d,\"sessions\":%d,\"total_cost_impact\":%.4f,\"severity\":\"%s\",\"pattern_id\":%s}",
      p, counts[p], session_counts[p], total_cost[p], severity_map[p], pattern_id_map[p]
  }
  printf "}"
}
' "$RECURRENCE_FILE")

# Generate promotion suggestions for patterns with 3+ occurrences across 2+ sessions
PROMOTION_SUGGESTIONS=$(echo "$RECURRENCE_JSON" | jq -r '
  to_entries |
  map(select(.value.occurrences >= 3 and .value.sessions >= 2)) |
  map({
    pattern: .key,
    pattern_id: .value.pattern_id,
    occurrences: .value.occurrences,
    sessions: .value.sessions,
    total_cost_impact: .value.total_cost_impact,
    severity: .value.severity,
    suggestion: ("Promote to AGENTS.md: Pattern \"" + .key + "\" has occurred " +
      (.value.occurrences | tostring) + " times across " +
      (.value.sessions | tostring) + " sessions. Add a prevention rule to AGENTS.md.")
  }) | sort_by(-.total_cost_impact)
' 2>/dev/null || echo "[]")

jq -n \
  --argjson analyzed "$SESSIONS_ANALYZED" \
  --argjson recurrence "$RECURRENCE_JSON" \
  --argjson promotions "$PROMOTION_SUGGESTIONS" \
  '{
    sessions_analyzed: $analyzed,
    pattern_recurrence: $recurrence,
    promotion_suggestions: $promotions
  }'
