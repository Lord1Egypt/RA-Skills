#!/usr/bin/env bash
# Conference Intern — Monitor for New Events
# Usage: bash scripts/monitor.sh <conference-id>
#
# Re-runs discover + curate, diffs against previous events.json to flag new events.

set -euo pipefail
source "$(dirname "$0")/common.sh"

CONFERENCE_ID=$(require_conference_id "${1:-}")
CONF_DIR=$(get_conf_dir "$CONFERENCE_ID")
CONFIG=$(load_config "$CONF_DIR")

EVENTS_FILE="$CONF_DIR/events.json"
PREVIOUS_FILE="$CONF_DIR/events-previous.json"

log_info "Monitoring for new events: $(config_get "$CONFIG" '.name')"

# Save current events as previous (for diffing)
if [ -f "$EVENTS_FILE" ]; then
  cp "$EVENTS_FILE" "$PREVIOUS_FILE"
  PREV_COUNT=$(jq 'length' "$PREVIOUS_FILE")
  log_info "Previous events snapshot: $PREV_COUNT events"
else
  echo "[]" > "$PREVIOUS_FILE"
  log_info "No previous events — first run, all events will be marked as new."
fi

# Run discover
log_info "--- Running discover ---"
bash "$SCRIPTS_DIR/discover.sh" "$CONFERENCE_ID"

# Check for new events
if [ -f "$EVENTS_FILE" ]; then
  NEW_COUNT=$(jq 'length' "$EVENTS_FILE")
  log_info "Events after discover: $NEW_COUNT"

  if [ "$NEW_COUNT" -eq 0 ]; then
    log_warn "No events found. Skipping curate."
    exit 0
  fi

  # Diff: find event IDs in current but not in previous
  NEW_IDS=$(jq -r '.[].id' "$EVENTS_FILE" | sort)
  OLD_IDS=$(jq -r '.[].id' "$PREVIOUS_FILE" 2>/dev/null | sort)
  ADDED=$(comm -23 <(echo "$NEW_IDS") <(echo "$OLD_IDS") | wc -l | tr -d ' ')
  REMOVED=$(comm -13 <(echo "$NEW_IDS") <(echo "$OLD_IDS") | wc -l | tr -d ' ')

  log_info "New events: $ADDED"
  log_info "Removed events: $REMOVED"

  if [ "$ADDED" -gt 0 ]; then
    echo ""
    echo "NEW EVENTS DETECTED:"
    # List new event names
    for id in $(comm -23 <(echo "$NEW_IDS") <(echo "$OLD_IDS")); do
      NAME=$(jq -r ".[] | select(.id == \"$id\") | .name" "$EVENTS_FILE")
      echo "  + $NAME"
    done
    echo ""
  fi
else
  log_error "events.json not found after discover."
  exit 1
fi

# Run curate
log_info "--- Running curate ---"
bash "$SCRIPTS_DIR/curate.sh" "$CONFERENCE_ID"

log_info "Monitor complete."
