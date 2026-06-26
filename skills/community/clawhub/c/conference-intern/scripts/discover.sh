#!/usr/bin/env bash
# Conference Intern — Discover Events (Script-Driven)
# Usage: bash scripts/discover.sh <conference-id>
#
# Fetches events from Luma pages (via agent) and Google Sheets (via curl/gog),
# merges, validates URLs, deduplicates, and writes events.json.

set -euo pipefail
source "$(dirname "$0")/common.sh"

CONFERENCE_ID=$(require_conference_id "${1:-}")
CONF_DIR=$(get_conf_dir "$CONFERENCE_ID")
CONFIG=$(load_config "$CONF_DIR")

EVENTS_FILE="$CONF_DIR/events.json"
SESSION_FILE="$CONF_DIR/luma-session.json"
DISCOVER_PROMPT=$(read_template "discover-luma-prompt.md")

# Initialize empty events array if no existing file
if [ ! -f "$EVENTS_FILE" ]; then
  echo "[]" > "$EVENTS_FILE"
fi

# Working set: accumulate all discovered events
WORKING_SET="[]"

log_info "Discovering events for: $(config_get "$CONFIG" '.name')"

# --- Temp file cleanup ---
RESULT_FILE=$(mktemp)
trap 'rm -f "$RESULT_FILE"' EXIT

# ==========================================================
# Phase 1: Luma URLs (primary source — CLI browser extraction)
# ==========================================================
LUMA_URLS=$(config_get "$CONFIG" '.luma_urls // [] | .[]' 2>/dev/null || true)

if [ -n "$LUMA_URLS" ] && [ "$LUMA_URLS" != "null" ]; then
  log_info "--- Luma sources (CLI browser) ---"
  LUMA_COUNT=0
  LUMA_EVENTS=0

  while IFS= read -r luma_url; do
    [ -z "$luma_url" ] || [ "$luma_url" = "null" ] && continue
    LUMA_COUNT=$((LUMA_COUNT + 1))
    log_info "[$LUMA_COUNT] Luma page: $luma_url"

    # Open page in browser
    TARGET_ID=$(openclaw browser open "$luma_url" 2>/dev/null | grep '^id:' | awk '{print $2}')
    if [ -z "$TARGET_ID" ]; then
      log_warn "  Failed to open page — skipping"
      continue
    fi
    log_info "  Page opened (target: ${TARGET_ID:0:8}...)"
    sleep 5  # initial page load

    # Scroll to load all events (infinite scroll)
    PREV_COUNT=0
    for scroll_i in $(seq 1 20); do
      CUR_COUNT=$(openclaw browser evaluate --target-id "$TARGET_ID" --fn 'async () => { window.scrollTo(0, document.documentElement.scrollHeight); await new Promise(r => setTimeout(r, 2000)); return document.querySelectorAll("[class*=card-wrapper]").length; }' 2>/dev/null)
      CUR_COUNT="${CUR_COUNT//[^0-9]/}"  # strip non-numeric
      [ -z "$CUR_COUNT" ] && CUR_COUNT=0
      log_info "  Scroll $scroll_i: $CUR_COUNT cards"
      if [ "$CUR_COUNT" -eq "$PREV_COUNT" ] && [ "$CUR_COUNT" -gt 0 ]; then
        log_info "  All events loaded"
        break
      fi
      PREV_COUNT="$CUR_COUNT"
    done

    # Bulk-extract all events in one JS evaluate call
    log_info "  Extracting events..."
    echo '[]' > "$RESULT_FILE"

    openclaw browser evaluate --target-id "$TARGET_ID" --fn '() => {
      const months = {"janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","août":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"};
      const events = [];
      let currentDate = "";
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
      let node;
      while (node = walker.nextNode()) {
        const cls = (typeof node.className === "string") ? node.className : "";
        if (cls.includes("content") && cls.includes("animated")) {
          const txt = node.textContent.trim();
          const dm = txt.match(/^(\d{1,2})\s*(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)/i);
          if (dm) currentDate = "2026-" + months[dm[2].toLowerCase()] + "-" + dm[1].padStart(2, "0");
        }
        if (cls.includes("card-wrapper")) {
          const link = node.querySelector("a.event-link");
          const href = link ? link.href : "";
          const ariaName = link ? (link.getAttribute("aria-label") || "") : "";
          const txt = node.textContent.replace(/\u200b/g, "").replace(/\s+/g, " ").trim();
          const tm = txt.match(/(\d{1,2}:\d{2})/);
          const time = tm ? tm[1] : "";
          const name = ariaName || txt.replace(/^\s*\d{1,2}:\d{2}\s*/, "").split(/Par /)[0].trim();
          const hostMatch = txt.match(/Par\s+(.+)/);
          let host = "";
          if (hostMatch) {
            host = hostMatch[1].split(/[·]/)[0].replace(/\s*(et|,)\s+/g, ", ").trim();
            host = host.replace(/\s*(Cannes|JW Marriott|Provence|Register|Liste|Participe|\+\d).*/i, "").trim();
          }
          const rsvpMatch = txt.match(/\+(\d[\d,.]*k?)/);
          let rsvpCount = null;
          if (rsvpMatch) { let n = rsvpMatch[1].replace(",", ""); if (n.endsWith("k")) n = parseFloat(n)*1000; rsvpCount = parseInt(n); }
          if (name) events.push({name, date: currentDate, time, host, rsvp_url: href, rsvp_count: rsvpCount, source: "luma"});
        }
      }
      return events;
    }' 2>/dev/null > "$RESULT_FILE"

    # Close the tab
    openclaw browser close --target-id "$TARGET_ID" 2>/dev/null || true

    # Read and validate result
    if [ -f "$RESULT_FILE" ] && jq 'type == "array"' "$RESULT_FILE" > /dev/null 2>&1; then
      PAGE_COUNT=$(jq 'length' "$RESULT_FILE")
      log_info "  Found $PAGE_COUNT events"
      LUMA_EVENTS=$((LUMA_EVENTS + PAGE_COUNT))
      WORKING_SET=$(echo "$WORKING_SET" | jq --slurpfile new "$RESULT_FILE" '. + $new[0]')
    else
      log_warn "  Invalid or empty result — skipping"
    fi

    sleep 5  # delay between URLs
  done <<< "$LUMA_URLS"

  log_info "Luma total: $LUMA_EVENTS events from $LUMA_COUNT pages"
else
  log_info "No Luma URLs configured — skipping Luma discovery"
fi

# ==========================================================
# Phase 2: Google Sheets (secondary source — browser extraction)
# ==========================================================
SHEETS=$(config_get "$CONFIG" '.sheets // [] | .[]' 2>/dev/null || true)

if [ -n "$SHEETS" ] && [ "$SHEETS" != "null" ]; then
  log_info "--- Google Sheets sources ---"
  SHEETS_EVENTS=0

  while IFS= read -r sheet_url; do
    [ -z "$sheet_url" ] || [ "$sheet_url" = "null" ] && continue
    log_info "Sheet: $sheet_url"

    echo '[]' > "$RESULT_FILE"

    SHEET_MSG="Open this Google Sheet in the browser and extract all event data.

URL: $sheet_url
RESULT_FILE: $RESULT_FILE

Read the spreadsheet and extract events. For each row, capture: name, date, time, location, description, host, rsvp_url, rsvp_count. Write a JSON array to the result file. Set source to \"sheets\" for all events. You MUST write to the exact path $RESULT_FILE. Close the tab when done."

    if timeout 300 openclaw agent --session-id "discover-$(date +%s)-$RANDOM" --message "$SHEET_MSG" > /dev/null 2>&1; then
      if [ -f "$RESULT_FILE" ] && jq 'type == "array"' "$RESULT_FILE" > /dev/null 2>&1; then
        SHEET_EVENTS=$(cat "$RESULT_FILE")
        SHEET_COUNT=$(echo "$SHEET_EVENTS" | jq 'length')
        log_info "  Found $SHEET_COUNT events"
      else
        log_warn "  Invalid or empty result — skipping"
        continue
      fi
    else
      EXIT_CODE=$?
      if [ "$EXIT_CODE" -eq 124 ]; then
        log_warn "  Agent timed out (300s) — skipping this sheet"
      else
        log_warn "  Agent exited with code $EXIT_CODE — skipping this sheet"
      fi
      continue
    fi

    # Merge sheets events: skip any that already exist in Luma set (by name only — date formats differ between sources)
    BEFORE=$(echo "$WORKING_SET" | jq 'length')
    WORKING_SET=$(echo "$WORKING_SET" | jq --argjson sheet "$SHEET_EVENTS" '
      . as $existing |
      ($existing | map({key: .name, value: true}) | from_entries) as $luma_keys |
      $sheet | map(select(.name as $n | $luma_keys[$n] != true)) |
      $existing + .
    ')
    ADDED=$(($(echo "$WORKING_SET" | jq 'length') - BEFORE))
    SHEETS_EVENTS=$((SHEETS_EVENTS + ADDED))
    log_info "  Added $ADDED new events (skipped duplicates from Luma)"
  done <<< "$SHEETS"

  log_info "Sheets total: $SHEETS_EVENTS new events"
else
  log_info "No Google Sheets configured — skipping Sheets discovery"
fi

# ==========================================================
# Phase 3: Post-processing
# ==========================================================
TOTAL=$(echo "$WORKING_SET" | jq 'length')
log_info "Total events before validation: $TOTAL"

if [ "$TOTAL" -eq 0 ]; then
  log_error "No events found from any source. Check your Luma URLs and Google Sheet links."
  exit 1
fi

# Set rsvp_status to "ok" for all events (skip slow per-URL HEAD validation)
# Dead links are caught at registration time when the page fails to load
log_info "Skipping URL validation (handled at registration time)..."
WORK_FILE=$(mktemp)
echo "$WORKING_SET" | jq '[.[] | . + {"rsvp_status": "ok"}]' > "$WORK_FILE"

# Generate IDs and set is_new flags
log_info "Generating IDs and checking for new events..."
EXISTING_IDS=""
if [ -f "$EVENTS_FILE" ] && [ "$(jq 'length' "$EVENTS_FILE")" -gt 0 ]; then
  EXISTING_IDS=$(jq -r '.[].id // empty' "$EVENTS_FILE" | sort -u)
fi

NEW_COUNT=0
VALIDATED_COUNT=$(jq 'length' "$WORK_FILE")
for i in $(seq 0 $((VALIDATED_COUNT - 1))); do
  NAME=$(jq -r ".[$i].name // \"\"" "$WORK_FILE")
  DATE=$(jq -r ".[$i].date // \"\"" "$WORK_FILE")
  TIME=$(jq -r ".[$i].time // \"\"" "$WORK_FILE")

  ID=$(generate_event_id "$NAME" "$DATE" "$TIME")

  IS_NEW=true
  if echo "$EXISTING_IDS" | grep -q "^${ID}$" 2>/dev/null; then
    IS_NEW=false
  else
    NEW_COUNT=$((NEW_COUNT + 1))
  fi

  WORK_FILE_TMP=$(jq --arg id "$ID" --argjson is_new "$IS_NEW" ".[$i].id = \$id | .[$i].is_new = \$is_new" "$WORK_FILE")
  echo "$WORK_FILE_TMP" > "$WORK_FILE"
done

# Write final events.json
cp "$WORK_FILE" "$EVENTS_FILE"
rm -f "$WORK_FILE"

FINAL_COUNT=$(jq 'length' "$EVENTS_FILE")
log_info "=== Discovery Complete ==="
log_info "  Total events: $FINAL_COUNT"
log_info "  New events: $NEW_COUNT"
log_info "  Saved to: $EVENTS_FILE"
