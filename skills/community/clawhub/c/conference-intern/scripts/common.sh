#!/usr/bin/env bash
# Shared helpers for conference-intern scripts
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"
TEMPLATES_DIR="$SKILL_DIR/templates"

# Workspace detection — conference data and runtime files live here
WORKSPACE_DIR=$(jq -r '.agents.defaults.workspace // empty' ~/.openclaw/openclaw.json 2>/dev/null)
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
CONFERENCES_DIR="$WORKSPACE_DIR/conferences"
KNOWLEDGE_FILE="$WORKSPACE_DIR/luma-knowledge.md"

# Logging
log_info()  { echo "[conference-intern] $*"; }
log_error() { echo "[conference-intern] ERROR: $*" >&2; }
log_warn()  { echo "[conference-intern] WARN: $*" >&2; }

# Validate conference-id argument
require_conference_id() {
  local id="${1:-}"
  if [ -z "$id" ]; then
    log_error "Usage: $0 <conference-id>"
    exit 1
  fi
  echo "$id"
}

# Get conference directory, ensure it exists
get_conf_dir() {
  local id="$1"
  local dir="$CONFERENCES_DIR/$id"
  if [ ! -d "$dir" ]; then
    log_error "Conference '$id' not found. Run setup first: bash scripts/setup.sh $id"
    exit 1
  fi
  echo "$dir"
}

# Get conference directory for setup (creates it)
init_conf_dir() {
  local id="$1"
  local dir="$CONFERENCES_DIR/$id"
  mkdir -p "$dir"
  echo "$dir"
}

# Load and validate config.json
load_config() {
  local conf_dir="$1"
  local config_file="$conf_dir/config.json"
  if [ ! -f "$config_file" ]; then
    log_error "No config.json found in $conf_dir. Run setup first."
    exit 1
  fi
  cat "$config_file"
}

# Read a field from config JSON
config_get() {
  local config="$1"
  local field="$2"
  echo "$config" | jq -r "$field"
}

# Check if gog CLI is available
has_gog() {
  command -v gog &>/dev/null
}

# Generate event ID: SHA-256 hash of name+date+time, truncated to 12 chars
generate_event_id() {
  local name="$1"
  local date="$2"
  local time="$3"
  echo -n "${name}${date}${time}" | sha256sum | cut -c1-12
}

# Read a prompt template
read_template() {
  local template_name="$1"
  local template_file="$TEMPLATES_DIR/$template_name"
  if [ ! -f "$template_file" ]; then
    log_error "Template not found: $template_file"
    exit 1
  fi
  cat "$template_file"
}

# Validate a Luma URL with a HEAD request
# Returns 0 if reachable (2xx/3xx), 1 if dead (4xx/5xx), 2 if timeout
validate_luma_url() {
  local url="$1"
  local status
  status=$(curl -sI -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null) || true
  if [ "$status" = "000" ]; then
    return 2  # timeout / connection failed
  elif [ "$status" -ge 200 ] && [ "$status" -lt 400 ]; then
    return 0  # reachable
  else
    return 1  # dead link
  fi
}

# Parse curated.md for events needing registration.
# Cross-references events.json to resolve RSVP URLs.
# Outputs tab-separated lines: event_name\trsvp_url
# Args: $1 = curated.md path, $2 = events.json path, $3 = mode ("all" or "pending-only"),
#       $4 = strategy ("aggressive" or "conservative")
#   aggressive:   include must_attend, recommended, optional. Skip blocked.
#   conservative: include must_attend, recommended only. Skip optional and blocked.
parse_registerable_events() {
  local curated_file="$1"
  local events_file="$2"
  local mode="${3:-all}"
  local strategy="${4:-aggressive}"

  local current_event=""
  local skip_event=false
  local found_pending=false
  local current_tier=""
  local -A seen=()

  # Returns 0 (include) or 1 (skip) based on tier and strategy
  _tier_included() {
    local tier="$1"
    # Custom tier override: "custom:must_attend,recommended"
    if [[ "$strategy" == custom:* ]]; then
      local allowed="${strategy#custom:}"
      if [[ ",$allowed," == *",$tier,"* ]]; then
        return 0
      else
        return 1
      fi
    fi
    case "$strategy" in
      conservative)
        case "$tier" in
          must_attend|recommended) return 0 ;;
          *) return 1 ;;
        esac
        ;;
      aggressive|*)
        case "$tier" in
          blocked) return 1 ;;
          *) return 0 ;;
        esac
        ;;
    esac
  }

  while IFS= read -r line; do
    # Detect section headers to track current tier
    if [[ "$line" =~ ^###\ Must\ Attend ]]; then
      current_tier="must_attend"
      continue
    elif [[ "$line" =~ ^###\ Recommended ]]; then
      current_tier="recommended"
      continue
    elif [[ "$line" =~ ^###\ Optional ]]; then
      current_tier="optional"
      continue
    elif [[ "$line" =~ ^##\ Blocked ]]; then
      current_tier="blocked"
      continue
    fi

    if [[ "$line" =~ ^-\ \*\*(.+)\*\*\ — ]]; then
      if [ -n "$current_event" ] && [ "$skip_event" = false ]; then
        if [ "$mode" = "all" ] || [ "$found_pending" = true ]; then
          if _tier_included "$current_tier" && [ -z "${seen[$current_event]+x}" ]; then
            _resolve_and_output "$current_event" "$events_file"
            seen["$current_event"]=1
          fi
        fi
      fi
      current_event="${BASH_REMATCH[1]}"
      skip_event=false
      found_pending=false
    elif [ -n "$current_event" ] && [ "$skip_event" = false ]; then
      if [[ "$line" =~ ✅|❌|🚫|🔗 ]]; then
        skip_event=true
      fi
      if [[ "$line" =~ ⏳ ]]; then
        found_pending=true
      fi
    fi
  done < "$curated_file"

  if [ -n "$current_event" ] && [ "$skip_event" = false ]; then
    if [ "$mode" = "all" ] || [ "$found_pending" = true ]; then
      if _tier_included "$current_tier" && [ -z "${seen[$current_event]+x}" ]; then
        _resolve_and_output "$current_event" "$events_file"
      fi
    fi
  fi
}

# Internal: look up an event's RSVP URL from events.json, filter to Luma URLs only
_resolve_and_output() {
  local event_name="$1"
  local events_file="$2"
  local rsvp_url
  rsvp_url=$(jq -r --arg name "$event_name" '
    .[] | select(.name == $name) | .rsvp_url // empty
  ' "$events_file" | head -1)

  # Only output Luma URLs (lu.ma or luma.com)
  if [ -n "$rsvp_url" ] && [[ "$rsvp_url" == *"lu.ma"* || "$rsvp_url" == *"luma.com"* ]]; then
    printf '%s\t%s\n' "$event_name" "$rsvp_url"
  fi
}

# Update an event's status in curated.md in-place.
# Finds the event by name, replaces or adds the status line below it.
# Args: $1 = curated.md path, $2 = event name, $3 = new status (e.g., "✅ Registered")
update_event_status() {
  local curated_file="$1"
  local event_name="$2"
  local new_status="$3"
  local tmp_file
  tmp_file=$(mktemp)

  local state="scanning"

  while IFS= read -r line; do
    case "$state" in
      scanning)
        echo "$line" >> "$tmp_file"
        if [[ "$line" == *"**${event_name}**"* ]]; then
          state="found"
        fi
        ;;
      found)
        if [[ "$line" =~ ^[[:space:]]+Host: ]]; then
          echo "$line" >> "$tmp_file"
          state="past_host"
        elif [[ "$line" =~ ^[[:space:]]+(✅|❌|🚫|🔗|🛑|🔒|⏳|📝) ]]; then
          echo "  $new_status" >> "$tmp_file"
          state="scanning"
        elif [[ "$line" == -* ]] || [[ ! "$line" =~ ^[[:space:]] ]]; then
          echo "  $new_status" >> "$tmp_file"
          echo "$line" >> "$tmp_file"
          state="scanning"
        else
          echo "$line" >> "$tmp_file"
        fi
        ;;
      past_host)
        if [[ "$line" =~ ^[[:space:]]+(✅|❌|🚫|🔗|🛑|🔒|⏳|📝) ]]; then
          echo "  $new_status" >> "$tmp_file"
          state="scanning"
        elif [[ "$line" == -* ]] || [[ ! "$line" =~ ^[[:space:]] ]] || [ -z "$line" ]; then
          echo "  $new_status" >> "$tmp_file"
          echo "$line" >> "$tmp_file"
          state="scanning"
        else
          echo "  $new_status" >> "$tmp_file"
          echo "$line" >> "$tmp_file"
          state="scanning"
        fi
        ;;
    esac
  done < "$curated_file"

  if [ "$state" != "scanning" ]; then
    echo "  $new_status" >> "$tmp_file"
  fi

  mv "$tmp_file" "$curated_file"
}

# Collect unique custom field labels from needs-input results,
# excluding fields already answered in custom-answers.json.
# Args: $1 = newline-separated list of "field1,field2" per event, $2 = custom-answers.json path (may not exist)
# Outputs: one field label per line
collect_unique_fields() {
  local fields_list="$1"
  local answers_file="${2:-}"
  local -A seen=()

  # Load existing answers
  local -A answered=()
  if [ -n "$answers_file" ] && [ -f "$answers_file" ]; then
    while IFS= read -r key; do
      answered["$key"]=1
    done < <(jq -r 'keys[]' "$answers_file" 2>/dev/null)
  fi

  # Deduplicate and filter
  while IFS= read -r fields_csv; do
    IFS=',' read -ra fields <<< "$fields_csv"
    for field in "${fields[@]}"; do
      field=$(echo "$field" | xargs)  # trim whitespace
      if [ -n "$field" ] && [ -z "${seen[$field]+x}" ] && [ -z "${answered[$field]+x}" ]; then
        seen["$field"]=1
        echo "$field"
      fi
    done
  done <<< "$fields_list"
}

# Parse Google Sheets CSV into event JSON array.
# Uses python3 for robust CSV handling (quoted fields, commas in values).
# Reads CSV from stdin, outputs JSON array to stdout.
# Skips rows with missing name or date.
parse_sheets_csv() {
  python3 -c '
import csv, json, sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)

# Map common header variations to our schema fields
HEADER_MAP = {
    "name": ["name", "event name", "event", "title", "event title"],
    "date": ["date", "event date", "start date", "day"],
    "time": ["time", "event time", "start time", "hours"],
    "location": ["location", "venue", "place", "address"],
    "description": ["description", "desc", "details", "about", "summary"],
    "host": ["host", "organizer", "organiser", "hosted by", "org"],
    "rsvp_url": ["url", "link", "rsvp", "rsvp url", "rsvp link", "registration", "register", "luma", "event url", "event link"],
    "rsvp_count": ["rsvps", "rsvp count", "attendees", "count", "going"],
}

def find_column(fieldnames, target_names):
    """Find the CSV column matching any of the target names (case-insensitive)."""
    for fn in fieldnames:
        if fn.strip().lower() in target_names:
            return fn
    return None

if not reader.fieldnames:
    print("[]")
    sys.exit(0)

col_map = {}
for schema_field, variations in HEADER_MAP.items():
    col = find_column(reader.fieldnames, variations)
    if col:
        col_map[schema_field] = col

events = []
for row in reader:
    name = row.get(col_map.get("name", ""), "").strip()
    date = row.get(col_map.get("date", ""), "").strip()
    if not name or not date:
        continue

    rsvp_count_str = row.get(col_map.get("rsvp_count", ""), "").strip()
    try:
        rsvp_count = int(rsvp_count_str) if rsvp_count_str else None
    except ValueError:
        rsvp_count = None

    events.append({
        "name": name,
        "date": date,
        "time": row.get(col_map.get("time", ""), "").strip() or "",
        "location": row.get(col_map.get("location", ""), "").strip() or "",
        "description": row.get(col_map.get("description", ""), "").strip() or "",
        "host": row.get(col_map.get("host", ""), "").strip() or "",
        "rsvp_url": row.get(col_map.get("rsvp_url", ""), "").strip() or "",
        "rsvp_count": rsvp_count,
        "source": "sheets",
    })

print(json.dumps(events))
'
}

# Register for a single Luma event using CLI browser commands.
# Agent is only called for fuzzy field matching when custom fields are present.
# Args: $1=rsvp_url, $2=result_file, $3=custom_answers_json (or empty), $4=knowledge_file
# Writes JSON result to $2.
cli_register_event() {
  local rsvp_url="$1"
  local result_file="$2"
  local custom_answers="${3:-}"
  local knowledge_file="${4:-}"

  # Known patterns
  local registered_patterns='["You'\''re registered", "You'\''re going", "Vous êtes inscrit", "Vous êtes déjà inscrit", "View your ticket", "Voir votre billet", "You'\''re on the waitlist", "Vous êtes sur la liste", "Pending approval", "already registered", "Votre inscription est en attente", "Your registration is pending"]'
  local register_btn_patterns='["register", "rsvp", "join", "participer", "s'\''inscrire", "request to join", "join waitlist", "request access", "demander", "liste d'\''attente"]'
  local captcha_patterns='["recaptcha", "hcaptcha"]'

  # Step 1: Open page
  local target_id
  target_id=$(openclaw browser open "$rsvp_url" 2>/dev/null | grep '^id:' | awk '{print $2}')
  if [ -z "$target_id" ]; then
    echo '{"status": "failed", "fields": [], "message": "Failed to open page"}' > "$result_file"
    return
  fi
  sleep 3

  # Step 2: Check already registered + captcha (full-text OK — these patterns are specific enough)
  local page_check
  page_check=$(openclaw browser evaluate --target-id "$target_id" --fn "() => {
    const body = document.body;
    const text = (body && body.innerText ? body.innerText : '').toLowerCase();
    const registered = $registered_patterns;
    const captcha = $captcha_patterns;
    if (document.querySelector('iframe[src*=captcha], iframe[src*=recaptcha], iframe[src*=hcaptcha], [class*=captcha], [class*=recaptcha], [class*=hcaptcha]') || captcha.some(p => text.includes(p.toLowerCase()))) return {status: 'captcha'};
    if (registered.some(p => text.includes(p.toLowerCase()))) return {status: 'registered'};
    return {status: 'open'};
  }" 2>/dev/null)

  local page_status
  page_status=$(echo "$page_check" | jq -r '.status // "open"' 2>/dev/null)

  if [ "$page_status" = "registered" ]; then
    echo '{"status": "registered", "fields": [], "message": "Already registered"}' > "$result_file"
    openclaw browser navigate --target-id "$target_id" "about:blank" 2>/dev/null || true; sleep 1; openclaw browser close --target-id "$target_id" 2>/dev/null || true
    return
  fi
  if [ "$page_status" = "captcha" ]; then
    echo '{"status": "captcha", "fields": [], "message": "CAPTCHA detected"}' > "$result_file"
    return
  fi

  # Step 3: Find and click Register/RSVP/Waitlist button
  local btn_result
  btn_result=$(openclaw browser evaluate --target-id "$target_id" --fn "() => {
    const patterns = $register_btn_patterns;
    const btns = [...document.querySelectorAll('button, a[role=button], [class*=btn], [class*=button], a.action-button')];
    for (const btn of btns) {
      const text = (btn.textContent || '').trim().toLowerCase();
      if (patterns.some(p => text.includes(p))) {
        btn.click();
        return {found: true, text: btn.textContent.trim()};
      }
    }
    return {found: false};
  }" 2>/dev/null)

  local btn_found
  btn_found=$(echo "$btn_result" | jq -r '.found // false' 2>/dev/null)

  if [ "$btn_found" != "true" ]; then
    # No button found — try agent fallback
    local agent_result
    agent_result=$(timeout 60 openclaw agent --session-id "regbtn-$(date +%s)-$RANDOM" --message "Open the browser tab with target ID $target_id. Find and click the registration/RSVP/waitlist button on this Luma event page. Just click it and reply with 'clicked' or 'not found'. Do not fill any forms." 2>&1 | tail -1)
    if [[ "$agent_result" != *"clicked"* ]] && [[ "$agent_result" != *"Clicked"* ]]; then
      # No button even with agent help — check if event is closed
      local closed_check
      closed_check=$(openclaw browser evaluate --target-id "$target_id" --fn '() => {
        const body = document.body;
        if (!body) return {closed: false};
        const text = body.innerText || "";
        const closedPhrases = [
          "cet événement affiche complet",
          "this event is sold out",
          "sold out",
          "registration closed",
          "inscriptions fermées",
          "event is full",
          "capacity reached"
        ];
        const lowerText = text.toLowerCase();
        for (const phrase of closedPhrases) {
          if (lowerText.includes(phrase)) return {closed: true, phrase: phrase};
        }
        return {closed: false};
      }' 2>/dev/null)

      local is_closed
      is_closed=$(echo "$closed_check" | jq -r '.closed // false' 2>/dev/null)

      if [ "$is_closed" = "true" ]; then
        echo '{"status": "closed", "fields": [], "message": "Event is full or registration closed"}' > "$result_file"
      else
        echo '{"status": "failed", "fields": [], "message": "Could not find register button"}' > "$result_file"
      fi
      openclaw browser navigate --target-id "$target_id" "about:blank" 2>/dev/null || true; sleep 1; openclaw browser close --target-id "$target_id" 2>/dev/null || true
      return
    fi
  fi

  sleep 2  # wait for form to appear

  # Verify tab is still alive before handing to agent
  if ! openclaw browser evaluate --target-id "$target_id" --fn '() => true' > /dev/null 2>&1; then
    echo '{"status": "failed", "fields": [], "message": "Tab died before form fill"}' > "$result_file"
    openclaw browser close --target-id "$target_id" 2>/dev/null || true
    return
  fi

  # Step 4: Hand off to agent for form filling
  local form_prompt
  form_prompt=$(read_template "register-single-prompt.md")

  local user_name="${USER_NAME:-}"
  local user_email="${USER_EMAIL:-}"

  local message="Fill and submit this Luma registration form.

TARGET_ID: $target_id
USER_NAME: $user_name
USER_EMAIL: $user_email
CUSTOM_ANSWERS: ${custom_answers:-(none)}
RESULT_FILE: $result_file

$form_prompt"

  if timeout 90 openclaw agent --session-id "regform-$(date +%s)-$RANDOM" --message "$message" > /dev/null 2>&1; then
    log_info "  Form agent completed"
  else
    local exit_code=$?
    if [ "$exit_code" -eq 124 ]; then
      log_warn "  Form agent timed out (90s)"
    else
      log_warn "  Form agent exited with code $exit_code"
    fi
  fi

  # Check if agent wrote a valid result
  local result_status
  result_status=$(jq -r '.status // ""' "$result_file" 2>/dev/null)
  if [ -z "$result_status" ] || [ "$result_status" = "" ] || [ "$result_status" = "null" ]; then
    echo '{"status": "failed", "fields": [], "message": "Agent did not write result"}' > "$result_file"
  fi

  # Validate agent status — only allow: registered, submitted, needs-input, failed
  # The CLI already handles closed/captcha/session-expired before the agent is called.
  # If the agent returns anything else, it's a misclassification — treat as failed (retryable).
  result_status=$(jq -r '.status // "failed"' "$result_file" 2>/dev/null)
  case "$result_status" in
    registered|submitted|needs-input|failed) ;; # valid
    *)
      local agent_msg
      agent_msg=$(jq -r '.message // ""' "$result_file" 2>/dev/null)
      echo "{\"status\": \"failed\", \"fields\": [], \"message\": \"Agent returned invalid status '$result_status': $agent_msg\"}" > "$result_file"
      ;;
  esac

  # Step 5: Close tab (agent doesn't handle this)
  openclaw browser navigate --target-id "$target_id" "about:blank" 2>/dev/null || true
  sleep 1
  openclaw browser close --target-id "$target_id" 2>/dev/null || true
}

# Collect events with non-Luma URLs from events.json.
# Returns JSON array of {name, url} for manual registration.
# Args: $1 = events.json path
collect_non_luma_events() {
  local events_file="$1"
  jq '[.[] | select(.rsvp_url != null and .rsvp_url != "" and (.rsvp_url | (contains("luma.com") or contains("lu.ma")) | not)) | {name: .name, url: .rsvp_url}]' "$events_file" 2>/dev/null || echo "[]"
}
