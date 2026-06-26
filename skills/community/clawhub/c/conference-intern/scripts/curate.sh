#!/usr/bin/env bash
# Conference Intern — Curate Events (Batch Processing)
# Usage: bash scripts/curate.sh <conference-id>
#
# Splits events into batches of 50, calls agent per batch for JSON scoring,
# merges results, generates curated.md with URL-based link markers.

set -euo pipefail
source "$(dirname "$0")/common.sh"

CONFERENCE_ID=$(require_conference_id "${1:-}")
CONF_DIR=$(get_conf_dir "$CONFERENCE_ID")
CONFIG=$(load_config "$CONF_DIR")

EVENTS_FILE="$CONF_DIR/events.json"
CURATED_FILE="$CONF_DIR/curated.md"
CURATE_PROMPT=$(read_template "curate-prompt.md")

BATCH_SIZE=50

if [ ! -f "$EVENTS_FILE" ]; then
  log_error "No events.json found. Run discover first: bash scripts/discover.sh $CONFERENCE_ID"
  exit 1
fi

EVENT_COUNT=$(jq 'length' "$EVENTS_FILE")
if [ "$EVENT_COUNT" -eq 0 ]; then
  log_warn "No events found in events.json. Nothing to curate."
  exit 0
fi

CONF_NAME=$(config_get "$CONFIG" '.name')
STRATEGY=$(config_get "$CONFIG" '.preferences.strategy')
INTERESTS=$(config_get "$CONFIG" '.preferences.interests | join(", ")')
AVOID=$(config_get "$CONFIG" '.preferences.avoid | join(", ")')
BLOCKED=$(config_get "$CONFIG" '.preferences.blocked_organizers | join(", ")')

log_info "Curating $EVENT_COUNT events for: $CONF_NAME"
log_info "Strategy: $STRATEGY | Batch size: $BATCH_SIZE"

# Compute summary stats for cross-batch calibration
STATS=$(jq '{
  total_events: length,
  rsvp_min: ([.[].rsvp_count | select(. != null)] | if length > 0 then min else 0 end),
  rsvp_max: ([.[].rsvp_count | select(. != null)] | if length > 0 then max else 0 end),
  rsvp_median: ([.[].rsvp_count | select(. != null)] | sort | if length > 0 then .[length/2 | floor] else 0 end),
  dates: ([.[].date] | unique | sort)
}' "$EVENTS_FILE")

log_info "Stats: $(echo "$STATS" | jq -c '{total: .total_events, rsvp_range: "\(.rsvp_min)-\(.rsvp_max)"}')"

# --- Batch curation ---
RESULT_FILE=$(mktemp)
ALL_RESULTS="[]"
trap 'rm -f "$RESULT_FILE"' EXIT

BATCH_NUM=0
OFFSET=0

while [ "$OFFSET" -lt "$EVENT_COUNT" ]; do
  BATCH_NUM=$((BATCH_NUM + 1))
  BATCH_END=$((OFFSET + BATCH_SIZE))
  [ "$BATCH_END" -gt "$EVENT_COUNT" ] && BATCH_END="$EVENT_COUNT"
  BATCH_COUNT=$((BATCH_END - OFFSET))

  log_info "Batch $BATCH_NUM: events $((OFFSET + 1))-$BATCH_END of $EVENT_COUNT"

  # Extract batch
  BATCH_JSON=$(jq ".[$OFFSET:$BATCH_END]" "$EVENTS_FILE")

  # Build message
  echo '[]' > "$RESULT_FILE"

  MESSAGE="Curate this batch of events. Write the JSON result to the specified file.

STRATEGY: $STRATEGY
INTERESTS: $INTERESTS
AVOID: $AVOID
BLOCKED_ORGANIZERS: $BLOCKED
STATS: $STATS
RESULT_FILE: $RESULT_FILE

EVENTS ($BATCH_COUNT in this batch, $EVENT_COUNT total):
$BATCH_JSON

$CURATE_PROMPT"

  if timeout 300 openclaw agent --session-id "curate-$(date +%s)-$RANDOM" --message "$MESSAGE" > /dev/null 2>&1; then
    log_info "  Agent completed"
  else
    EXIT_CODE=$?
    if [ "$EXIT_CODE" -eq 124 ]; then
      log_error "  Batch $BATCH_NUM timed out (300s)"
    else
      log_error "  Batch $BATCH_NUM failed with exit code $EXIT_CODE"
    fi
    OFFSET=$BATCH_END
    continue
  fi

  # Read and validate batch result
  if [ -f "$RESULT_FILE" ] && jq 'type == "array"' "$RESULT_FILE" > /dev/null 2>&1; then
    BATCH_RESULT_COUNT=$(jq 'length' "$RESULT_FILE")
    log_info "  Scored $BATCH_RESULT_COUNT events"
    ALL_RESULTS=$(echo "$ALL_RESULTS" | jq --slurpfile batch "$RESULT_FILE" '. + $batch[0]')
  else
    log_warn "  Invalid result — skipping batch"
  fi

  OFFSET=$BATCH_END
  sleep 5  # delay between batches
done

TOTAL_SCORED=$(echo "$ALL_RESULTS" | jq 'length')
log_info "Total scored: $TOTAL_SCORED / $EVENT_COUNT"

if [ "$TOTAL_SCORED" -eq 0 ]; then
  log_error "No events were scored. Curation failed."
  exit 1
fi

# --- Generate curated.md from merged JSON ---
log_info "Generating curated.md..."

python3 -c "
import json, sys
from datetime import datetime

events_file = '$EVENTS_FILE'
results_json = sys.stdin.read()
conf_name = '$CONF_NAME'
strategy = '$STRATEGY'

with open(events_file) as f:
    events = json.load(f)

results = json.loads(results_json)
events_by_name = {e['name']: e for e in events}
results_by_name = {r['name']: r for r in results}

# Merge: for each result, attach event details
merged = []
for r in results:
    e = events_by_name.get(r['name'], {})
    merged.append({**e, 'tier': r.get('tier', 'optional'), 'reason': r.get('reason', '')})

# Add events not in results (agent dropped them) as 'optional'
scored_names = set(r['name'] for r in results)
for e in events:
    if e['name'] not in scored_names:
        merged.append({**e, 'tier': 'optional', 'reason': 'Not scored by curation agent'})

# Group by date then tier
from collections import defaultdict
by_date = defaultdict(lambda: defaultdict(list))
blocked = []
for e in merged:
    if e['tier'] == 'blocked':
        blocked.append(e)
    else:
        date = e.get('date', 'Unknown')
        by_date[date][e['tier']].append(e)

# Determine link marker based on URL
def link_marker(e):
    url = e.get('rsvp_url', '') or ''
    if 'luma.com' in url or 'lu.ma' in url:
        return ''
    elif url:
        return f'  🔗 [Register manually]({url})'
    else:
        return '  🔗 No registration link'

# Render markdown
tier_order = ['must_attend', 'recommended', 'optional']
tier_labels = {'must_attend': 'Must Attend', 'recommended': 'Recommended', 'optional': 'Optional'}

lines = []
lines.append(f'# {conf_name} — Side Events')
lines.append(f'')
now = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
total = len(merged)
recommended = sum(1 for e in merged if e['tier'] in ('must_attend', 'recommended'))
lines.append(f'Last updated: {now} UTC')
lines.append(f'Strategy: {strategy} | Events: {total} found, {recommended} recommended')
lines.append('')

for date in sorted(by_date.keys()):
    lines.append(f'## {date}')
    lines.append('')
    tiers = by_date[date]
    for tier in tier_order:
        if tier in tiers and tiers[tier]:
            lines.append(f'### {tier_labels[tier]}')
            for e in sorted(tiers[tier], key=lambda x: x.get('time', '')):
                name = e.get('name', '?')
                time = e.get('time', '')
                location = e.get('location', '')
                host = e.get('host', '')
                rsvp_count = e.get('rsvp_count')
                at_loc = f' @ {location}' if location else ''
                lines.append(f'- **{name}** — {time}{at_loc}')
                host_line = f'  Host: {host}' if host else ''
                if rsvp_count:
                    host_line += f' | RSVPs: {rsvp_count}'
                if host_line:
                    lines.append(host_line)
                marker = link_marker(e)
                if marker:
                    lines.append(marker)
            lines.append('')

if blocked:
    lines.append('## Blocked / Filtered Out')
    for e in blocked:
        lines.append(f'- ~~{e.get(\"name\", \"?\")}~~ — {e.get(\"reason\", \"blocked\")}')
    lines.append('')

print('\n'.join(lines))
" <<< "$ALL_RESULTS" > "$CURATED_FILE"

# Verify
TOTAL_LISTED=$(grep -c "^- \*\*" "$CURATED_FILE" 2>/dev/null || echo "0")
BLOCKED_COUNT=$(grep -c "^- ~~" "$CURATED_FILE" 2>/dev/null || echo "0")
MANUAL_COUNT=$(grep -c "🔗" "$CURATED_FILE" 2>/dev/null || echo "0")

log_info "=== Curation Complete ==="
log_info "  Events listed: $TOTAL_LISTED"
log_info "  Blocked/filtered: $BLOCKED_COUNT"
log_info "  Manual registration: $MANUAL_COUNT"
log_info "  Saved to: $CURATED_FILE"
