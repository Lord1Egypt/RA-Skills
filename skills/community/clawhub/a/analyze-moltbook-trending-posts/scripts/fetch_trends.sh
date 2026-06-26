#!/bin/bash
# fetch_trends.sh — Fetch Moltbook trending posts via API
# Usage: bash fetch_trends.sh
# Env overrides: SUBMOLTS, TIMEFRAMES, PAGES, PAGE_SIZE, DELAY_MS, SORT_MODE, SNAPSHOT_DIR

set -euo pipefail

# ---------- defaults ----------
SUBMOLTS="${SUBMOLTS:-general,agents}"
TIMEFRAMES="${TIMEFRAMES:-hour,day,week}"
PAGES="${PAGES:-3}"
PAGE_SIZE="${PAGE_SIZE:-100}"
DELAY_MS="${DELAY_MS:-1500}"
SORT_MODE="${SORT_MODE:-top}"
API_ROOT="https://www.moltbook.com/api/v1"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SNAPSHOT_DIR="${SNAPSHOT_DIR:-$SKILL_ROOT/data/snapshots}"

TIMESTAMP="$(date -u +%Y-%m-%d_%H%M)"

# ---------- helpers ----------
log()  { echo "[fetch] $(date -u +%H:%M:%S) $*"; }
die()  { echo "[fetch] FATAL: $*" >&2; exit 1; }

delay_seconds() {
  # convert ms to fractional seconds for sleep
  python3 -c "print(${DELAY_MS}/1000.0)" 2>/dev/null || echo "1.5"
}

DELAY_SEC="$(delay_seconds)"

# --fail-with-body requires curl 7.76+; fall back to --fail if unavailable
CURL_FAIL_FLAG="--fail-with-body"
curl --fail-with-body --version >/dev/null 2>&1 || CURL_FAIL_FLAG="--fail"

mkdir -p "$SNAPSHOT_DIR"

# ---------- fetch one page ----------
# Args: submolt, sort_mode, timeframe, page, page_size
# Prints: JSON response body
fetch_page() {
  local submolt="$1" sort_mode="$2" timeframe="$3" page="$4" page_size="$5"
  local encoded_submolt
  encoded_submolt="$(echo -n "$submolt" | python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read()))")"
  local url="${API_ROOT}/submolts/${encoded_submolt}/feed"
  local params="sort=${sort_mode}&limit=${page_size}&page=${page}"

  # time param only applies to top and comments sort modes
  if [[ "$sort_mode" == "top" || "$sort_mode" == "comments" ]]; then
    params="${params}&time=${timeframe}"
  fi

  curl -sS $CURL_FAIL_FLAG \
    -H "Accept: application/json" \
    "${url}?${params}" 2>&1
}

# ---------- main loop ----------
SAVED_FILES=()
TOTAL_POSTS=0
TOTAL_PAGES=0
START_MS=$(python3 -c "import time; print(int(time.time()*1000))")

IFS=',' read -ra SUBMOLT_ARR <<< "$SUBMOLTS"
IFS=',' read -ra TIMEFRAME_ARR <<< "$TIMEFRAMES"

for submolt in "${SUBMOLT_ARR[@]}"; do
  submolt="$(echo "$submolt" | xargs)"  # trim whitespace
  for timeframe in "${TIMEFRAME_ARR[@]}"; do
    timeframe="$(echo "$timeframe" | xargs)"
    log "Fetching submolt=$submolt timeframe=$timeframe sort=$SORT_MODE pages=$PAGES"

    ALL_POSTS="[]"
    FETCHED=0
    PAGES_DONE=0
    STOP_REASON="target reached"

    for (( page=1; page<=PAGES; page++ )); do
      log "  page $page/$PAGES ..."

      RESPONSE="$(fetch_page "$submolt" "$SORT_MODE" "$timeframe" "$page" "$PAGE_SIZE")" || {
        log "  WARNING: page $page failed, stopping pagination for this combo"
        STOP_REASON="fetch error on page $page"
        break
      }

      # Extract posts array and count
      PAGE_POSTS="$(python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
posts = data.get('posts', [])
print(json.dumps(posts))
" <<< "$RESPONSE")"

      PAGE_COUNT="$(python3 -c "import json,sys; print(len(json.loads(sys.stdin.read())))" <<< "$PAGE_POSTS")"

      if [[ "$PAGE_COUNT" -eq 0 ]]; then
        log "  page $page returned 0 posts — stopping pagination"
        STOP_REASON="empty page"
        break
      fi

      # Merge into ALL_POSTS (both passed via stdin to avoid shell quoting issues)
      ALL_POSTS="$(printf '%s\n' "$ALL_POSTS" "$PAGE_POSTS" | python3 -c "
import json, sys
lines = sys.stdin.read().rstrip().split('\n')
existing = json.loads(lines[0])
new = json.loads(lines[1])
existing.extend(new)
print(json.dumps(existing))
")"

      FETCHED=$((FETCHED + PAGE_COUNT))
      PAGES_DONE=$((PAGES_DONE + 1))
      TOTAL_PAGES=$((TOTAL_PAGES + 1))
      log "  got $PAGE_COUNT posts (total so far: $FETCHED)"

      # Rate limiting — skip delay on last page
      if [[ "$page" -lt "$PAGES" && "$PAGE_COUNT" -gt 0 ]]; then
        sleep "$DELAY_SEC"
      fi
    done

    TOTAL_POSTS=$((TOTAL_POSTS + FETCHED))

    if [[ "$FETCHED" -eq 0 ]]; then
      log "  no posts fetched for $submolt/$timeframe — skipping snapshot"
      continue
    fi

    # Build snapshot JSON (pass config via env vars to avoid shell quoting issues)
    OUTFILE="${SNAPSHOT_DIR}/${TIMESTAMP}_${submolt}_${timeframe}.json"

    _SUBMOLT="$submolt" \
    _SORT_MODE="$SORT_MODE" \
    _TIMEFRAME="$timeframe" \
    _PAGE_SIZE="$PAGE_SIZE" \
    _PAGES="$PAGES" \
    _PAGES_DONE="$PAGES_DONE" \
    _STOP_REASON="$STOP_REASON" \
    _OUTFILE="$OUTFILE" \
    python3 -c "
import json, sys, os, uuid
from datetime import datetime, timezone

posts = json.loads(sys.stdin.read())

# Compute summary stats
scores = [p.get('upvotes',0) - p.get('downvotes',0) for p in posts]
comments = [p.get('comment_count',0) for p in posts]
authors = set(p.get('author',{}).get('name','') for p in posts if p.get('author'))

avg_score = sum(scores)/len(scores) if scores else 0
max_score = max(scores) if scores else 0
avg_comments = sum(comments)/len(comments) if comments else 0

snapshot = {
    'version': 1,
    'id': str(uuid.uuid4()),
    'createdAt': datetime.now(timezone.utc).isoformat(),
    'source': 'moltbook-trend-analysis',
    'request': {
        'submolt': os.environ['_SUBMOLT'],
        'sortMode': os.environ['_SORT_MODE'],
        'timeframe': os.environ['_TIMEFRAME'],
        'pageSize': int(os.environ['_PAGE_SIZE']),
        'resultCount': len(posts),
        'pagesRequested': int(os.environ['_PAGES']),
        'pagesFetched': int(os.environ['_PAGES_DONE']),
        'stopReason': os.environ['_STOP_REASON']
    },
    'meta': {
        'totalFetched': len(posts),
        'totalPages': int(os.environ['_PAGES_DONE']),
        'durationMs': None  # per-combo timing not tracked
    },
    'summary': {
        'avgScore': round(avg_score, 2),
        'maxScore': max_score,
        'avgComments': round(avg_comments, 2),
        'uniqueAuthors': len(authors)
    },
    'posts': posts
}

outfile = os.environ['_OUTFILE']
with open(outfile, 'w') as f:
    json.dump(snapshot, f, indent=2, ensure_ascii=False)

print(outfile)
" <<< "$ALL_POSTS"

    SAVED_FILES+=("$OUTFILE")
    log "  saved: $OUTFILE ($FETCHED posts)"
  done
done

END_MS=$(python3 -c "import time; print(int(time.time()*1000))")
DURATION_MS=$((END_MS - START_MS))

echo ""
echo "========================================"
echo "Fetch complete."
echo "  Total posts:     $TOTAL_POSTS"
echo "  Total API pages: $TOTAL_PAGES"
echo "  Duration:        ~${DURATION_MS}ms"
echo "  Snapshot files:"
if [[ ${#SAVED_FILES[@]} -gt 0 ]]; then
  for f in "${SAVED_FILES[@]}"; do
    echo "    $f"
  done
else
  echo "    (none)"
fi
echo "========================================"
