#!/usr/bin/env bash
# Conference Intern — Register for Events (Batch Processing)
# Usage: bash scripts/register.sh <conference-id> [--retry-pending] [--batch-size <n>] [--tier <tiers>]
#
# Processes events in batches. Each run handles --batch-size events (default 10),
# writes registration-status.json, and exits. The agent reads the status, asks the
# user for custom field answers, then re-runs for the next batch.

set -euo pipefail
source "$(dirname "$0")/common.sh"

# --- Parse arguments ---
CONFERENCE_ID=""
RETRY_PENDING=false
BATCH_SIZE=10
DELAY=15
TIER_OVERRIDE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --retry-pending) RETRY_PENDING=true; shift ;;
    --batch-size)
      if [ -z "${2:-}" ] || ! [[ "$2" =~ ^[0-9]+$ ]]; then
        log_error "--batch-size requires a positive integer"
        exit 1
      fi
      BATCH_SIZE="$2"; shift 2 ;;
    --tier)
      if [ -z "${2:-}" ]; then
        log_error "--tier requires a value (e.g., must_attend, must_attend,recommended)"
        exit 1
      fi
      TIER_OVERRIDE="$2"; shift 2 ;;
    -*) log_error "Unknown flag: $1"; exit 1 ;;
    *) CONFERENCE_ID="$1"; shift ;;
  esac
done

CONFERENCE_ID=$(require_conference_id "$CONFERENCE_ID")
CONF_DIR=$(get_conf_dir "$CONFERENCE_ID")
CONFIG=$(load_config "$CONF_DIR")

CURATED_FILE="$CONF_DIR/curated.md"
EVENTS_FILE="$CONF_DIR/events.json"
SESSION_FILE="$CONF_DIR/luma-session.json"
ANSWERS_FILE="$CONF_DIR/custom-answers.json"
STATUS_FILE="$CONF_DIR/registration-status.json"

USER_NAME=$(config_get "$CONFIG" '.user_info.name')
USER_EMAIL=$(config_get "$CONFIG" '.user_info.email')
STRATEGY=$(config_get "$CONFIG" '.preferences.strategy // "aggressive"')

if [ ! -f "$CURATED_FILE" ]; then
  log_error "No curated.md found. Run curate first: bash scripts/curate.sh $CONFERENCE_ID"
  exit 1
fi

if [ ! -f "$EVENTS_FILE" ]; then
  log_error "No events.json found. Run discover first: bash scripts/discover.sh $CONFERENCE_ID"
  exit 1
fi

# --- Determine effective strategy for tier filtering ---
if [ -n "$TIER_OVERRIDE" ]; then
  # --tier flag overrides strategy-based filtering
  EFFECTIVE_STRATEGY="custom:$TIER_OVERRIDE"
  log_info "Registering for events: $(config_get "$CONFIG" '.name')"
  log_info "Batch size: $BATCH_SIZE | Delay: ${DELAY}s | Tiers: $TIER_OVERRIDE"
else
  EFFECTIVE_STRATEGY="$STRATEGY"
  log_info "Registering for events: $(config_get "$CONFIG" '.name')"
  log_info "Batch size: $BATCH_SIZE | Delay: ${DELAY}s | Strategy: $STRATEGY"
fi

# --- Determine parse mode ---
PARSE_MODE="all"
if [ "$RETRY_PENDING" = true ]; then
  PARSE_MODE="pending-only"
  log_info "Retry-pending mode: processing only ⏳ Needs input events"
fi

# --- Build event list ---
EVENTS_LIST=""
while IFS=$'\t' read -r name url; do
  EVENTS_LIST+="${name}"$'\t'"${url}"$'\n'
done < <(parse_registerable_events "$CURATED_FILE" "$EVENTS_FILE" "$PARSE_MODE" "$EFFECTIVE_STRATEGY")

if [ -z "$EVENTS_LIST" ]; then
  log_info "No events to register. All events already have terminal status."
  echo '{"batch_size":'"$BATCH_SIZE"',"processed_this_batch":0,"remaining":0,"results_this_batch":{"registered":0,"needs_input":0,"failed":0,"closed":0},"new_fields":[],"all_needs_input_fields":[],"done":true}' | jq '.' > "$STATUS_FILE"
  exit 0
fi

TOTAL_COUNT=$(echo -n "$EVENTS_LIST" | grep -c '.' || true)
log_info "Found $TOTAL_COUNT events to process (batch of $BATCH_SIZE)"

# --- Load existing custom answers ---
CUSTOM_ANSWERS=""
if [ -f "$ANSWERS_FILE" ]; then
  CUSTOM_ANSWERS=$(cat "$ANSWERS_FILE")
  log_info "Loaded existing custom answers from $ANSWERS_FILE"
fi

# --- Counters ---
REGISTERED=0
NEEDS_INPUT=0
FAILED=0
CLOSED=0
BATCH_NUM=0

# --- Temp file cleanup ---
RESULT_FILE=$(mktemp)
NEEDS_INPUT_FIELDS_FILE=$(mktemp)
trap 'rm -f "$RESULT_FILE" "$NEEDS_INPUT_FIELDS_FILE"' EXIT

# --- Batch loop ---
while IFS=$'\t' read -r EVENT_NAME RSVP_URL; do
  [ -z "$EVENT_NAME" ] && continue
  BATCH_NUM=$((BATCH_NUM + 1))

  # Stop after batch_size events
  if [ "$BATCH_NUM" -gt "$BATCH_SIZE" ]; then
    break
  fi

  log_info "[$BATCH_NUM/$BATCH_SIZE] $EVENT_NAME"
  log_info "  URL: $RSVP_URL"

  # Clear previous result
  echo '{}' > "$RESULT_FILE"

  # Register using CLI browser commands
  if ! cli_register_event "$RSVP_URL" "$RESULT_FILE" "$CUSTOM_ANSWERS" "$KNOWLEDGE_FILE"; then
    echo '{"status": "failed", "fields": [], "message": "Registration helper crashed"}' > "$RESULT_FILE"
  fi

  # Parse result
  STATUS=$(jq -r '.status // "failed"' "$RESULT_FILE" 2>/dev/null || echo "failed")
  FIELDS_JSON=$(jq '.fields // []' "$RESULT_FILE" 2>/dev/null || echo "[]")
  FIELDS_DISPLAY=$(echo "$FIELDS_JSON" | jq -r 'join(", ")' 2>/dev/null || echo "")
  MSG=$(jq -r '.message // ""' "$RESULT_FILE" 2>/dev/null || echo "")

  log_info "  Status: $STATUS${MSG:+ — $MSG}"

  case "$STATUS" in
    registered)
      update_event_status "$CURATED_FILE" "$EVENT_NAME" "✅ Registered"
      REGISTERED=$((REGISTERED + 1))
      ;;
    submitted)
      update_event_status "$CURATED_FILE" "$EVENT_NAME" "📝 Submitted"
      REGISTERED=$((REGISTERED + 1))
      ;;
    needs-input)
      update_event_status "$CURATED_FILE" "$EVENT_NAME" "⏳ Needs input: [$FIELDS_DISPLAY]"
      NEEDS_INPUT=$((NEEDS_INPUT + 1))
      # Append each field as a separate line (no comma splitting)
      echo "$FIELDS_JSON" | jq -r '.[]' 2>/dev/null >> "$NEEDS_INPUT_FIELDS_FILE"
      ;;
    closed)
      update_event_status "$CURATED_FILE" "$EVENT_NAME" "🚫 Closed"
      CLOSED=$((CLOSED + 1))
      ;;
    captcha)
      update_event_status "$CURATED_FILE" "$EVENT_NAME" "🛑 CAPTCHA"
      log_error "CAPTCHA detected — stopping batch."
      break
      ;;
    session-expired)
      update_event_status "$CURATED_FILE" "$EVENT_NAME" "🔒 Session expired"
      log_error "Session expired — stopping batch."
      break
      ;;
    failed|*)
      update_event_status "$CURATED_FILE" "$EVENT_NAME" "❌ Failed${MSG:+: $MSG}"
      FAILED=$((FAILED + 1))
      ;;
  esac

  # Delay between events (skip after last in batch)
  if [ "$BATCH_NUM" -lt "$BATCH_SIZE" ]; then
    sleep "$DELAY"
  fi

done <<< "$EVENTS_LIST"

# --- Calculate remaining ---
PROCESSED=$((REGISTERED + NEEDS_INPUT + FAILED + CLOSED))
REMAINING=$((TOTAL_COUNT - PROCESSED))
[ "$REMAINING" -lt 0 ] && REMAINING=0

# --- Collect new custom fields not yet in answers ---
NEW_FIELDS="[]"
ALL_FIELDS="[]"
if [ -s "$NEEDS_INPUT_FIELDS_FILE" ]; then
  ALL_FIELDS=$(sort -u "$NEEDS_INPUT_FIELDS_FILE" | grep -v '^$' | jq -R . | jq -s '.')
  if [ -f "$ANSWERS_FILE" ]; then
    KNOWN_KEYS=$(jq -r 'keys[]' "$ANSWERS_FILE" 2>/dev/null)
    NEW_FIELDS=$(echo "$ALL_FIELDS" | jq --argjson known "$(echo "$KNOWN_KEYS" | jq -R . | jq -s '.')" '[.[] | select(. as $f | $known | index($f) | not)]')
  else
    NEW_FIELDS="$ALL_FIELDS"
  fi
fi

# --- Write status file ---
DONE=false
if [ "$REMAINING" -eq 0 ]; then
  DONE=true
fi

# Collect non-Luma events for manual registration
MANUAL_REG=$(collect_non_luma_events "$EVENTS_FILE")

jq -n \
  --argjson batch_size "$BATCH_SIZE" \
  --argjson processed "$PROCESSED" \
  --argjson remaining "$REMAINING" \
  --argjson registered "$REGISTERED" \
  --argjson needs_input "$NEEDS_INPUT" \
  --argjson failed "$FAILED" \
  --argjson closed "$CLOSED" \
  --argjson new_fields "$NEW_FIELDS" \
  --argjson all_fields "$ALL_FIELDS" \
  --argjson done "$DONE" \
  --argjson manual "$MANUAL_REG" \
  '{
    batch_size: $batch_size,
    processed_this_batch: $processed,
    remaining: $remaining,
    results_this_batch: {
      registered: $registered,
      needs_input: $needs_input,
      failed: $failed,
      closed: $closed
    },
    new_fields: $new_fields,
    all_needs_input_fields: $all_fields,
    done: $done,
    manual_registration: $manual
  }' > "$STATUS_FILE"

# --- Summary ---
echo ""
log_info "=== Batch Summary ==="
log_info "  ✅ Registered: $REGISTERED"
log_info "  ⏳ Needs input: $NEEDS_INPUT"
log_info "  🚫 Closed: $CLOSED"
log_info "  ❌ Failed: $FAILED"
log_info "  Remaining: $REMAINING"
log_info "  Status written to: $STATUS_FILE"

if [ "$DONE" = true ]; then
  log_info "All events processed."
else
  log_info "Run again to process next batch."
fi
