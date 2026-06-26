#!/usr/bin/env bash
set -euo pipefail

VERSION="0.12.0"

# headline.sh [--brief] <sessions-directory>
# Scans all recent sessions (last 7 days), runs diagnose on each,
# produces tweetable headline block or brief one-liner.
# Output is formatted text (not JSON).

usage() {
  cat <<EOF
Usage: headline.sh [--help|--version] [--brief] <sessions-directory>

Description:
  Scans recent sessions, outputs tweetable health check or brief one-liner.

Options:
  --help      Show this help message and exit
  --version   Show version and exit
  --brief     Output a single-line summary instead of the full headline block

Example:
  headline.sh ~/.openclaw/agents/main/sessions/
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

BRIEF=0
SESSIONS_DIR=""

while [ $# -gt 0 ]; do
  case "$1" in
    --help) usage; exit 0 ;;
    --version) echo "$VERSION"; exit 0 ;;
    --brief) BRIEF=1; shift ;;
    *) SESSIONS_DIR="$1"; shift ;;
  esac
done

check_deps

if [ -z "$SESSIONS_DIR" ]; then
  echo "Usage: headline.sh [--brief] <sessions-directory>" >&2
  exit 1
fi

if [ ! -d "$SESSIONS_DIR" ]; then
  echo "Error: directory not found: $SESSIONS_DIR" >&2
  exit 1
fi

# Collect JSONL files modified in last 7 days
SESSION_FILES=()
while IFS= read -r -d '' f; do
  SESSION_FILES+=("$f")
done < <(find "$SESSIONS_DIR" -name "*.jsonl" -newer /dev/null -print0 2>/dev/null || true)

# Fallback: just grab all jsonl files if find with -newer fails
if [ ${#SESSION_FILES[@]} -eq 0 ]; then
  while IFS= read -r -d '' f; do
    SESSION_FILES+=("$f")
  done < <(find "$SESSIONS_DIR" -name "*.jsonl" -print0 2>/dev/null || true)
fi

TOTAL_SESSIONS=${#SESSION_FILES[@]}

if [ "$TOTAL_SESSIONS" -eq 0 ]; then
  if [ "$BRIEF" -eq 1 ]; then
    echo "No sessions found in $SESSIONS_DIR"
  else
    echo "🩻 clawdoc — no sessions found in $SESSIONS_DIR"
  fi
  exit 0
fi

# Run diagnose on each session, collect all findings
ALL_FINDINGS_FILE=$(mktemp /tmp/clawdoc_findings.XXXXXX)
trap 'rm -f "$ALL_FINDINGS_FILE"' EXIT

TOTAL_COST=0
TOTAL_WASTE=0
TOTAL_FINDINGS=0

for f in "${SESSION_FILES[@]}"; do
  # Get session cost
  sess_cost=$(jq -s '[.[] | select(.type=="message" and .message.role=="assistant") | .message.usage.cost.total // 0] | add // 0' "$f" 2>/dev/null || echo 0)
  TOTAL_COST=$(echo "$TOTAL_COST + $sess_cost" | awk '{printf "%.6f", $1+$3}' 2>/dev/null || echo "$TOTAL_COST")

  # Run diagnose (suppress stderr)
  findings=$(bash "$DIAGNOSE" "$f" 2>/dev/null || echo "[]")
  echo "$findings" >> "$ALL_FINDINGS_FILE"
done

# Aggregate all findings
COMBINED=$(jq -s '[.[][] ]' "$ALL_FINDINGS_FILE" 2>/dev/null || echo "[]")
TOTAL_FINDINGS=$(echo "$COMBINED" | jq 'length' 2>/dev/null || echo 0)
TOTAL_WASTE=$(echo "$COMBINED" | jq '[.[].cost_impact // 0] | add // 0' 2>/dev/null || echo 0)

# Compute recoverable percentage
RECOVERABLE_PCT=0
if [ "$(echo "$TOTAL_COST > 0" | awk '{print ($1 > 0)}')" = "1" ]; then
  RECOVERABLE_PCT=$(echo "$TOTAL_WASTE $TOTAL_COST" | awk '{if($2>0) printf "%d", ($1/$2)*100; else print 0}')
fi

if [ "$BRIEF" -eq 1 ]; then
  # Brief one-liner
  YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d 'yesterday' +%Y-%m-%d 2>/dev/null || echo "yesterday")
  WARN_COUNT=$(echo "$COMBINED" | jq '[.[] | select(.severity == "critical" or .severity == "high")] | length' 2>/dev/null || echo 0)
  TOP_PATTERN=$(echo "$COMBINED" | jq -r 'sort_by(-.cost_impact // 0) | first | if . then .pattern else empty end' 2>/dev/null || echo "")

  if [ "$TOTAL_FINDINGS" -eq 0 ]; then
    printf "%s: %d sessions, \$%.2f, all clear\n" "$YESTERDAY" "$TOTAL_SESSIONS" "$TOTAL_COST"
  elif [ -n "$TOP_PATTERN" ]; then
    printf "%s: %d sessions, \$%.2f, %d alert(s) (%s)\n" \
      "$YESTERDAY" "$TOTAL_SESSIONS" "$TOTAL_COST" "$WARN_COUNT" "$TOP_PATTERN"
  else
    printf "%s: %d sessions, \$%.2f, %d finding(s)\n" \
      "$YESTERDAY" "$TOTAL_SESSIONS" "$TOTAL_COST" "$TOTAL_FINDINGS"
  fi
  exit 0
fi

# Full headline mode
printf "🩻 clawdoc — %d finding(s) across %d session(s) (last 7 days)\n" "$TOTAL_FINDINGS" "$TOTAL_SESSIONS"
printf "💸 \$%.2f spent" "$TOTAL_COST"
if [ "$TOTAL_FINDINGS" -gt 0 ]; then
  printf " — \$%.2f was waste (%d%% recoverable)" "$TOTAL_WASTE" "$RECOVERABLE_PCT"
fi
printf "\n"

# Print top findings by severity (critical first, then high, then medium)
# Strip absolute paths from evidence to avoid leaking filesystem info in shared channels
echo "$COMBINED" | jq -r '
  sort_by(
    if .severity == "critical" then 0
    elif .severity == "high" then 1
    elif .severity == "medium" then 2
    else 3 end,
    -(.cost_impact // 0)
  ) | .[:5][] |
  (if .severity == "critical" then "🔴"
   elif .severity == "high" then "🟠"
   elif .severity == "medium" then "🟡"
   else "🟢" end) + " " + (.evidence | gsub("/[Uu]sers/[^/]+/"; "~/") | gsub("/home/[^/]+/"; "~/") | gsub("/private/tmp/[^/]+/"; "/tmp/"))
' 2>/dev/null || true
