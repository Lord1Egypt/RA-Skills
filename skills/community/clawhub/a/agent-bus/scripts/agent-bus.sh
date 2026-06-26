#!/usr/bin/env bash
# =============================================================================
# agent-bus.sh — Agent Bus CLI
# Version: v0.6 | 2026-03-30
# Purpose: All Agent Bus repo operations must go through this script.
#          Do NOT directly read/write repo files.
# =============================================================================

set -euo pipefail

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
REPO_DIR="${AGENT_BUS_REPO:-$(cd "$(dirname "$0")" && pwd)}"
ACL_FILE="${AGENT_BUS_ACL:-$HOME/.agent-bus/acl.json}"
STATE_FILE="${AGENT_BUS_STATE:-$HOME/.agent-bus/state.json}"
USAGE_FILE="${AGENT_BUS_USAGE:-$HOME/.agent-bus/usage.json}"
NOTIF_FILE="${AGENT_BUS_NOTIF:-$HOME/.agent-bus/notified.json}"
MY_ID_FILE="${AGENT_BUS_ID:-$HOME/.agent-bus/agent-id}"

# Hard limits
MAX_AUTH_DAYS=365
MAX_AUTH_TASKS=10000
DEFAULT_AUTH_DAYS=7
DEFAULT_AUTH_TASKS=10

# Expiry warning threshold (days before expiry)
EXPIRY_WARN_DAYS=7

# Sensitive keyword blocklist (scanned before writing any message to the repo)
COMPANY_KEYWORDS=(
  "internal.company.com" "corp.intranet"
  "salary" "payroll" "api_secret" "private_key"
  "internal network" "vpn credentials"
)

# Prompt injection detection patterns
INJECTION_PATTERNS=(
  "ignore.{0,20}instruction"
  "forget.{0,20}previous"
  "you are now"
  "new system prompt"
  "system prompt"
  "reveal.{0,30}(password|secret|token|cookie|key)"
  "\[INST\]|\[SYS\]|\[SYSTEM\]"
  "<script|<iframe|javascript:"
  "sudo |rm -rf|curl .* \| bash|wget .* \| sh"
)

HIGH_RISK_KEYWORDS=(
  "token" "cookie" "secret" "password" "private key"
  "update-acl" "agents.json"
)

MAX_CONTENT_LENGTH=2000
MAX_TASKS_PER_HOUR=999999
INACTIVE_DAYS=30

# --------------------------------------------------------------------------
# Utilities
# --------------------------------------------------------------------------
log_info()  { echo "[INFO]  $*" >&2; }
log_warn()  { echo "[WARN]  $*" >&2; }
log_error() { echo "[ERROR] $*" >&2; }

die() { log_error "$*"; exit 1; }

get_my_id() {
  [[ -f "$MY_ID_FILE" ]] || die "Agent ID not initialized. Run: agent-bus.sh init <agent-id>"
  cat "$MY_ID_FILE"
}

acl_get() {
  local key="$1"
  [[ -f "$ACL_FILE" ]] || die "ACL file not found. Run: agent-bus.sh init"
  python3 -c "
import json
with open('$ACL_FILE') as f:
    acl = json.load(f)
val = acl.get('$key', [])
print(' '.join(val) if isinstance(val, list) else val)
"
}

check_acl() {
  local direction="$1" agent_id="$2"
  local allowed
  allowed=$(acl_get "$direction")
  for id in $allowed; do [[ "$id" == "$agent_id" ]] && return 0; done
  return 1
}

scan_company_keywords() {
  local content="$1"
  for kw in "${COMPANY_KEYWORDS[@]}"; do
    if echo "$content" | grep -qi "$kw"; then
      die "Message contains a blocked keyword '$kw'. Ensure no sensitive information is included."
    fi
  done
}

scan_injection() {
  local content="$1"
  for pattern in "${INJECTION_PATTERNS[@]}"; do
    if echo "$content" | grep -qiE "$pattern" 2>/dev/null; then
      die "Possible prompt injection detected (pattern: $pattern). Message rejected. Notify your owner to check the message source."
    fi
  done
}

check_length() {
  local content="$1"
  local len=${#content}
  if (( len > MAX_CONTENT_LENGTH )); then
    die "Message exceeds max length (${len} > ${MAX_CONTENT_LENGTH} chars). Message rejected."
  fi
}

ts_now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
date_now() { date -u +%Y-%m-%d; }
make_ts_slug() { date -u +%Y%m%d%H%M%S; }

# --------------------------------------------------------------------------
# Local usage tracker (not stored in repo — local only)
# --------------------------------------------------------------------------
usage_get_sent() {
  local ref="$1"
  python3 - <<EOF
import json, os
f = '$USAGE_FILE'
if not os.path.exists(f):
    print(0); exit()
with open(f) as fh:
    data = json.load(fh)
print(data.get('sent', {}).get('$ref', {}).get('tasks_sent', 0))
EOF
}

usage_get_received() {
  local ref="$1"
  python3 - <<EOF
import json, os
f = '$USAGE_FILE'
if not os.path.exists(f):
    print(0); exit()
with open(f) as fh:
    data = json.load(fh)
print(data.get('received', {}).get('$ref', {}).get('tasks_received', 0))
EOF
}

usage_inc_sent() {
  local ref="$1"
  python3 - <<EOF
import json, os
from datetime import datetime, timezone
f = '$USAGE_FILE'
data = json.load(open(f)) if os.path.exists(f) else {}
data.setdefault('sent', {}).setdefault('$ref', {'tasks_sent': 0, 'last_sent': ''})
data['sent']['$ref']['tasks_sent'] += 1
data['sent']['$ref']['last_sent'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
with open(f, 'w') as fh:
    json.dump(data, fh, indent=2)
EOF
}

usage_inc_received() {
  local ref="$1"
  python3 - <<EOF
import json, os
from datetime import datetime, timezone
f = '$USAGE_FILE'
data = json.load(open(f)) if os.path.exists(f) else {}
data.setdefault('received', {}).setdefault('$ref', {'tasks_received': 0, 'last_received': ''})
data['received']['$ref']['tasks_received'] += 1
data['received']['$ref']['last_received'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
with open(f, 'w') as fh:
    json.dump(data, fh, indent=2)
EOF
}

# --------------------------------------------------------------------------
# Pair relationship validation
# --------------------------------------------------------------------------

# Read pair mode from agents.json (returns bidirectional / a→b / b→a, or empty)
find_pair_mode() {
  local a="$1" b="$2"
  python3 - <<EOF
import json, sys
try:
    with open('$REPO_DIR/shared/agents.json') as f:
        data = json.load(f)
    for p in data.get('pairs', []):
        if (p['a'] == '$a' and p['b'] == '$b') or (p['a'] == '$b' and p['b'] == '$a'):
            print(p.get('mode', ''))
            sys.exit(0)
    print('')
except:
    print('')
EOF
}

# Check if a pair has been revoked
is_pair_revoked() {
  local a="$1" b="$2"
  local revoked_a revoked_b
  revoked_a=$(find "$REPO_DIR/responses" -name "pair_revoked_${a}↔${b}_*.md" 2>/dev/null | head -1)
  revoked_b=$(find "$REPO_DIR/responses" -name "pair_revoked_${b}↔${a}_*.md" 2>/dev/null | head -1)
  [[ -n "$revoked_a" || -n "$revoked_b" ]]
}

# Read a field value from a response/request file
res_get() {
  local res_file="$1" field="$2"
  grep "^${field}:" "$res_file" | sed "s/^${field}: *//" | tr -d '"'
}

# Core pair validation: check if $from can send $type message to $to
# Returns 0=allowed, 1=denied
check_pair() {
  local from="$1" to="$2" type="$3"

  # Non-task messages (reply/sync/notify): only require a pair to exist
  if [[ "$type" != "task" ]]; then
    local mode
    mode=$(find_pair_mode "$from" "$to")
    if [[ -z "$mode" ]]; then
      log_warn "No pair relationship between '$from' and '$to'. Message rejected."
      return 1
    fi
    return 0
  fi

  # Task messages: strict directional check
  local mode
  mode=$(find_pair_mode "$from" "$to")

  if [[ -z "$mode" ]]; then
    log_warn "No pair relationship between '$from' and '$to'. Task rejected."
    return 1
  fi

  if is_pair_revoked "$from" "$to"; then
    log_warn "Pair relationship '$from' ↔ '$to' has been revoked. Task rejected."
    return 1
  fi

  case "$mode" in
    bidirectional) return 0 ;;
    "a→b")
      local pair_a
      pair_a=$(python3 -c "
import json
with open('$REPO_DIR/shared/agents.json') as f:
    data = json.load(f)
for p in data.get('pairs', []):
    if (p['a'] == '$from' and p['b'] == '$to') or (p['a'] == '$to' and p['b'] == '$from'):
        print(p['a']); break
")
      if [[ "$from" == "$pair_a" ]]; then return 0; fi
      log_warn "Pair mode is a→b. '$from' cannot send tasks to '$to' (only '$pair_a' can initiate tasks)."
      return 1
      ;;
    "b→a")
      local pair_b
      pair_b=$(python3 -c "
import json
with open('$REPO_DIR/shared/agents.json') as f:
    data = json.load(f)
for p in data.get('pairs', []):
    if (p['a'] == '$from' and p['b'] == '$to') or (p['a'] == '$to' and p['b'] == '$from'):
        print(p['b']); break
")
      if [[ "$from" == "$pair_b" ]]; then return 0; fi
      log_warn "Pair mode is b→a. '$from' cannot send tasks to '$to' (only '$pair_b' can initiate tasks)."
      return 1
      ;;
    *)
      log_warn "Unknown pair mode '$mode'. Rejected."
      return 1
      ;;
  esac
}

# --------------------------------------------------------------------------
# Command: pair-request
# --------------------------------------------------------------------------
cmd_pair_request() {
  local with_id="" mode="bidirectional" reason="" features=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --with)     with_id="${2:-}"; shift 2 ;;
      --mode)     mode="${2:-}"; shift 2 ;;
      --reason)   reason="${2:-}"; shift 2 ;;
      --features) features="${2:-}"; shift 2 ;;
      *) die "Unknown argument: $1" ;;
    esac
  done
  [[ -z "$with_id" ]] && die "Usage: agent-bus.sh pair-request --with <agent-id> [--mode bidirectional|a→b|b→a] [--features memory-sync,...] --reason <reason>"
  [[ -z "$reason" ]] && die "--reason is required"

  case "$mode" in
    bidirectional|a→b|b→a) ;;
    *) die "Invalid mode '$mode'. Valid values: bidirectional / a→b / b→a" ;;
  esac

  # Validate features (comma-separated; only known features allowed)
  if [[ -n "$features" ]]; then
    local KNOWN_FEATURES="memory-sync file-share config-push"
    IFS=',' read -ra feat_list <<< "$features"
    for feat in "${feat_list[@]}"; do
      feat=$(echo "$feat" | tr -d ' ')
      local ok=0
      for kf in $KNOWN_FEATURES; do [[ "$feat" == "$kf" ]] && ok=1 && break; done
      if (( ok == 0 )); then
        die "Unknown feature '$feat'. Known features: $KNOWN_FEATURES"
      fi
    done
  fi

  local my_id ts_slug
  my_id=$(get_my_id)
  ts_slug=$(make_ts_slug)

  local existing_mode
  existing_mode=$(find_pair_mode "$my_id" "$with_id")
  if [[ -n "$existing_mode" ]]; then
    die "'$my_id' and '$with_id' are already paired (mode: $existing_mode). No need to re-request."
  fi

  mkdir -p "$REPO_DIR/requests"
  local req_file="$REPO_DIR/requests/pair_${my_id}↔${with_id}_${ts_slug}.md"

  cat > "$req_file" <<EOF
type: pair_request
from: ${my_id}
to: ${with_id}
reason: "${reason}"
timestamp: $(ts_now)
status: pending

proposed_mode: ${mode}
proposed_features: ${features}
EOF

  cd "$REPO_DIR"
  git add "$req_file"
  git commit -m "pair-request: ${my_id}↔${with_id} @ ${ts_slug}" --quiet
  git push origin main --quiet

  log_info "Pair request submitted: $(basename "$req_file")"
  echo "========================================"
  echo "Pair request sent to '$with_id'"
  echo "  File:            $(basename "$req_file")"
  echo "  Proposed mode:   ${mode}"
  echo "  Proposed features: ${features:-none}"
  echo "  Reason:          ${reason}"
  echo ""
  echo "Notify your owner: 'Pair request sent to ${with_id}, waiting for their owner to approve.'"
  echo "Tasks cannot be sent to '$with_id' until the request is approved."
  echo "========================================"
}

# --------------------------------------------------------------------------
# Command: approve-pair
# --------------------------------------------------------------------------
cmd_approve_pair() {
  local req_basename="" override_mode="" override_features=""
  req_basename="${1:-}"
  shift || true
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --mode)     override_mode="${2:-}"; shift 2 ;;
      --features) override_features="${2:-}"; shift 2 ;;
      *) die "Unknown argument: $1" ;;
    esac
  done
  [[ -z "$req_basename" ]] && die "Usage: agent-bus.sh approve-pair <pair_req_filename> [--mode a→b|b→a] [--features memory-sync,...]"

  local req_file="$REPO_DIR/requests/${req_basename}"
  [[ -f "$req_file" ]] || die "Request file not found: ${req_basename}"

  local my_id req_from req_reason proposed_mode proposed_features
  my_id=$(get_my_id)
  req_from=$(res_get "$req_file" "from")
  req_reason=$(res_get "$req_file" "reason")
  proposed_mode=$(res_get "$req_file" "proposed_mode")
  proposed_features=$(res_get "$req_file" "proposed_features")

  # Narrowing rule for mode: can only restrict, not expand
  local final_mode="${proposed_mode}"
  if [[ -n "$override_mode" ]]; then
    if [[ "$proposed_mode" == "bidirectional" ]]; then
      case "$override_mode" in
        bidirectional|a→b|b→a) final_mode="$override_mode" ;;
        *) die "Invalid mode: ${override_mode}" ;;
      esac
    else
      if [[ "$override_mode" == "bidirectional" ]]; then
        die "Cannot expand scope: request was '$proposed_mode', cannot change to bidirectional"
      fi
      final_mode="$override_mode"
    fi
  fi

  # Features: approver can only remove features, not add new ones
  # If --features not specified, grant all proposed features
  local final_features="${proposed_features}"
  if [[ -n "$override_features" ]]; then
    # Validate that override_features is a subset of proposed_features
    IFS=',' read -ra req_feats <<< "$proposed_features"
    IFS=',' read -ra override_feats <<< "$override_features"
    for feat in "${override_feats[@]}"; do
      feat=$(echo "$feat" | tr -d ' ')
      local allowed=0
      for rf in "${req_feats[@]}"; do
        rf=$(echo "$rf" | tr -d ' ')
        [[ "$feat" == "$rf" ]] && allowed=1 && break
      done
      if (( allowed == 0 )); then
        die "Cannot grant feature '$feat' that was not in the original request (proposed: $proposed_features)"
      fi
    done
    final_features="$override_features"
  fi

  local ts_slug
  ts_slug=$(make_ts_slug)
  local res_file="$REPO_DIR/responses/pair_res_${req_from}↔${my_id}_${ts_slug}.md"

  mkdir -p "$REPO_DIR/responses"
  cat > "$res_file" <<EOF
type: pair_response
from: ${my_id}
to: ${req_from}
request_ref: ${req_basename}
decision: approved
authorized_by: owner
timestamp: $(ts_now)

granted_mode: ${final_mode}
granted_features: ${final_features}
EOF

  sed -i 's/^status: pending$/status: approved/' "$req_file"

  # Update agents.json: add both agents + pair entry (with features)
  python3 - <<EOF
import json, os
from datetime import datetime, timezone
agents_file = '$REPO_DIR/shared/agents.json'
data = json.load(open(agents_file)) if os.path.exists(agents_file) else {"version": "2", "agents": [], "pairs": []}
data.setdefault('agents', [])
data.setdefault('pairs', [])

ids = [a['id'] for a in data['agents']]
for aid in ['$req_from', '$my_id']:
    if aid not in ids:
        data['agents'].append({"id": aid, "name": aid})

pair_ids = [(p['a'], p['b']) for p in data['pairs']]
if ('$req_from', '$my_id') not in pair_ids and ('$my_id', '$req_from') not in pair_ids:
    features_str = '$final_features'
    features_list = [f.strip() for f in features_str.split(',') if f.strip()] if features_str else []
    data['pairs'].append({
        "a": "$req_from",
        "b": "$my_id",
        "mode": "$final_mode",
        "features": features_list,
        "established": datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        "approvedBy": "owner",
        "pairRef": "$(basename "$res_file")"
    })

with open(agents_file, 'w') as f:
    json.dump(data, f, indent=2)
print("agents.json updated")
EOF

  mkdir -p "$REPO_DIR/inbox/${req_from}"
  [[ ! -f "$REPO_DIR/inbox/${req_from}/.gitkeep" ]] && touch "$REPO_DIR/inbox/${req_from}/.gitkeep"

  cmd_update_acl "allowReceiveFrom" "$req_from" "add" 2>/dev/null || true
  cmd_update_acl "allowSendTo" "$req_from" "add" 2>/dev/null || true

  cd "$REPO_DIR"
  git add "$res_file" "$req_file" "shared/agents.json" "inbox/${req_from}/"
  git commit -m "pair-approved: ${req_from}↔${my_id} mode=${final_mode} features=${final_features} @ ${ts_slug}" --quiet
  git push origin main --quiet

  echo "========================================"
  echo "Pair request from '$req_from' approved."
  echo "  Mode:           ${final_mode}"
  echo "  Features:       ${final_features:-none}"
  echo "  Response file:  $(basename "$res_file")"
  echo ""
  echo "'$req_from' will receive the response on their next poll and their owner will be notified."
  echo "========================================"

  # Auto-sync ACL so the new pair partner can communicate immediately
  cmd_sync_acl
}

# --------------------------------------------------------------------------
# Command: reject-pair
# --------------------------------------------------------------------------
cmd_reject_pair() {
  local req_basename="${1:-}"
  [[ -z "$req_basename" ]] && die "Usage: agent-bus.sh reject-pair <pair_req_filename>"

  local req_file="$REPO_DIR/requests/${req_basename}"
  [[ -f "$req_file" ]] || die "Request file not found: ${req_basename}"

  local my_id req_from ts_slug
  my_id=$(get_my_id)
  req_from=$(res_get "$req_file" "from")
  ts_slug=$(make_ts_slug)

  local res_file="$REPO_DIR/responses/pair_res_${req_from}↔${my_id}_${ts_slug}.md"
  mkdir -p "$REPO_DIR/responses"
  cat > "$res_file" <<EOF
type: pair_response
from: ${my_id}
to: ${req_from}
request_ref: ${req_basename}
decision: rejected
authorized_by: owner
timestamp: $(ts_now)
EOF

  sed -i 's/^status: pending$/status: rejected/' "$req_file"

  cd "$REPO_DIR"
  git add "$res_file" "$req_file"
  git commit -m "pair-rejected: ${req_from}↔${my_id} @ ${ts_slug}" --quiet
  git push origin main --quiet

  echo "========================================"
  echo "Pair request from '$req_from' rejected."
  echo "'$req_from' will receive the rejection on their next poll and their owner will be notified."
  echo "========================================"
}

# --------------------------------------------------------------------------
# Command: revoke-pair
# --------------------------------------------------------------------------
cmd_revoke_pair() {
  local pair_ref="${1:-}"
  [[ -z "$pair_ref" ]] && die "Usage: agent-bus.sh revoke-pair <other-agent-id>"

  local my_id ts_slug
  my_id=$(get_my_id)
  ts_slug=$(make_ts_slug)

  local other_id="$pair_ref"
  if [[ "$pair_ref" == *"↔"* ]]; then
    other_id=$(echo "$pair_ref" | sed 's/pair_res_//' | sed "s/↔${my_id}_.*//;s/.*↔//" | tr -d '_0-9' || echo "$pair_ref")
  fi

  local existing_mode
  existing_mode=$(find_pair_mode "$my_id" "$other_id")
  [[ -z "$existing_mode" ]] && die "No pair relationship between '$my_id' and '$other_id'."

  local revoke_file="$REPO_DIR/responses/pair_revoked_${my_id}↔${other_id}_${ts_slug}.md"
  mkdir -p "$REPO_DIR/responses"
  cat > "$revoke_file" <<EOF
type: pair_revoked
from: ${my_id}
to: ${other_id}
timestamp: $(ts_now)
reason: "revoked by owner"
EOF

  # Remove pair from agents.json
  python3 - <<EOF
import json, os
agents_file = '$REPO_DIR/shared/agents.json'
if not os.path.exists(agents_file):
    print("agents.json not found, skipping"); exit()
data = json.load(open(agents_file))
before = len(data.get('pairs', []))
data['pairs'] = [p for p in data.get('pairs', [])
                 if not ((p['a'] in ['$my_id','$other_id']) and (p['b'] in ['$my_id','$other_id']))]
after = len(data['pairs'])
with open(agents_file, 'w') as f:
    json.dump(data, f, indent=2)
print(f"Removed {before-after} pair(s)")
EOF

  cmd_update_acl "allowReceiveFrom" "$other_id" "remove" 2>/dev/null || true
  cmd_update_acl "allowSendTo" "$other_id" "remove" 2>/dev/null || true

  # Notify the other agent
  local notify_file="$REPO_DIR/inbox/${other_id}/$(make_ts_slug)-${my_id}-notify.md"
  mkdir -p "$REPO_DIR/inbox/${other_id}"
  cat > "$notify_file" <<EOF
type: notify
from: ${my_id}
to: ${other_id}
subject: "pair revoked"
timestamp: $(ts_now)
status: unread
pair_ref:
---

'${my_id}' owner has revoked the pair relationship with '${other_id}'.
Please update your local agents.json and ACL.
EOF

  cd "$REPO_DIR"
  git add "$revoke_file" "shared/agents.json" "$notify_file"
  git commit -m "pair-revoked: ${my_id}↔${other_id} @ ${ts_slug}" --quiet
  git push origin main --quiet

  echo "========================================"
  echo "Pair revoked: ${my_id} ↔ ${other_id}"
  echo "The other agent will be notified on their next poll."
  echo "========================================"
}

# --------------------------------------------------------------------------
# Check for pending pair requests (directed at me)
# --------------------------------------------------------------------------
check_pending_pairs() {
  local my_id
  my_id=$(get_my_id)
  [[ -d "$REPO_DIR/requests" ]] || return 0

  for f in "$REPO_DIR/requests"/pair_*↔${my_id}_*.md; do
    [[ -f "$f" ]] || continue
    local status
    status=$(res_get "$f" "status")
    [[ "$status" != "pending" ]] && continue

    local req_from req_reason proposed_mode
    req_from=$(res_get "$f" "from")
    req_reason=$(res_get "$f" "reason")
    proposed_mode=$(res_get "$f" "proposed_mode")

    echo "========================================"
    echo "[Pair Request] From: '${req_from}'"
    echo "  File:          $(basename "$f")"
    echo "  Reason:        ${req_reason}"
    echo "  Proposed mode: ${proposed_mode}"
    echo ""
    echo "Notify your owner. To respond:"
    echo "  Approve:          ./agent-bus.sh approve-pair $(basename "$f")"
    echo "  Approve (narrow): ./agent-bus.sh approve-pair $(basename "$f") --mode a→b"
    echo "  Reject:           ./agent-bus.sh reject-pair  $(basename "$f")"
    echo "========================================"
  done
}

# --------------------------------------------------------------------------
# Check for pair revocation notifications
# --------------------------------------------------------------------------
check_revoke_notifications() {
  local my_id
  my_id=$(get_my_id)
  [[ -d "$REPO_DIR/responses" ]] || return 0

  for f in "$REPO_DIR/responses"/pair_revoked_*↔${my_id}_*.md \
           "$REPO_DIR/responses"/pair_revoked_${my_id}↔*_*.md; do
    [[ -f "$f" ]] || continue
    local notified_key="revoke_$(basename "$f")"
    if [[ -f "$NOTIF_FILE" ]] && python3 -c "
import json
with open('$NOTIF_FILE') as fh:
    d = json.load(fh)
print('yes' if '$notified_key' in d.get('notified', []) else 'no')
" 2>/dev/null | grep -q "yes"; then
      continue
    fi

    local other_from other_to
    other_from=$(res_get "$f" "from")
    other_to=$(res_get "$f" "to")

    echo "========================================"
    echo "Pair relationship has been revoked."
    echo "  Revoked by: ${other_from}"
    echo "  Affected:   ${other_from} ↔ ${other_to} communication terminated"
    echo ""
    echo "Update your local ACL (after owner confirmation):"
    echo "  ./agent-bus.sh update-acl allowReceiveFrom ${other_from} remove"
    echo "  ./agent-bus.sh update-acl allowSendTo      ${other_from} remove"
    echo "========================================"

    python3 - <<EOF
import json, os
f = '$NOTIF_FILE'
data = json.load(open(f)) if os.path.exists(f) else {'notified': []}
data.setdefault('notified', [])
if '$notified_key' not in data['notified']:
    data['notified'].append('$notified_key')
with open(f, 'w') as fh:
    json.dump(data, fh, indent=2)
EOF
  done
}

# --------------------------------------------------------------------------
# Risk assessment
# --------------------------------------------------------------------------
RISK_LEVEL="green"
RISK_REASONS=()

assess_risk() {
  local from="$1" content="$2" type="${3:-task}"
  RISK_LEVEL="green"
  RISK_REASONS=()

  # Red: high-risk keywords
  for kw in "${HIGH_RISK_KEYWORDS[@]}"; do
    if echo "$content" | grep -qi "$kw"; then
      RISK_LEVEL="red"
      RISK_REASONS+=("Content contains high-risk keyword '$kw'")
    fi
  done

  # Yellow (B13): rate-limit — send to pending instead of auto-reject
  if [[ -f "$STATE_FILE" ]]; then
    local count_1h
    count_1h=$(python3 - <<EOF
import json, time
with open('$STATE_FILE') as f:
    state = json.load(f)
tasks_1h = state.get('senderHistory', {}).get('$from', {}).get('tasks_last_1h', [])
now = time.time()
print(len([t for t in tasks_1h if now - t < 3600]))
EOF
)
    if (( count_1h >= MAX_TASKS_PER_HOUR )); then
      # B13: rate-limit -> pending (owner decides), not auto-reject
      RISK_LEVEL="yellow"
      RISK_REASONS+=("rate-limit: Sender '$from' sent ${count_1h} tasks in the last hour (limit: ${MAX_TASKS_PER_HOUR})")
    fi
  fi

  [[ "$RISK_LEVEL" == "red" ]] && return

  # Yellow: first-time sender
  if [[ -f "$STATE_FILE" ]]; then
    local is_first
    is_first=$(python3 -c "
import json
with open('$STATE_FILE') as f:
    state = json.load(f)
print('yes' if '$from' not in state.get('senderHistory', {}) else 'no')
")
    [[ "$is_first" == "yes" ]] && { RISK_LEVEL="yellow"; RISK_REASONS+=("First-time sender: '$from'"); }
  fi

  # Yellow: long-inactive sender
  if [[ -f "$STATE_FILE" ]]; then
    local days_inactive
    # O1: use sys.argv to pass $from, avoid heredoc shell variable expansion warning
    days_inactive=$(python3 -c "
import json, time, sys
from datetime import datetime, timezone
from_arg = sys.argv[1]
state_file = sys.argv[2]
try:
    with open(state_file) as f:
        state = json.load(f)
    last = state.get('senderHistory', {}).get(from_arg, {}).get('lastActive', '')
    if not last:
        print(9999)
    else:
        print(int((time.time() - datetime.fromisoformat(last.replace('Z','+00:00')).timestamp()) / 86400))
except:
    print(9999)
" "$from" "$STATE_FILE")
    if (( days_inactive >= INACTIVE_DAYS )); then
      RISK_LEVEL="yellow"
      RISK_REASONS+=("Sender '$from' has been inactive for ${days_inactive} days")
    fi
  fi

  # Yellow: bulk/heavy operations
  for kw in "all records" "bulk" "crawl" "batch" "full scan"; do
    if echo "$content" | grep -qi "$kw"; then
      RISK_LEVEL="yellow"; RISK_REASONS+=("Task contains bulk operation keyword '$kw'"); break
    fi
  done

  # Yellow: external URLs (non-GitHub)
  if echo "$content" | grep -qiE "https?://[^ ]+"; then
    local url
    url=$(echo "$content" | grep -oiE "https?://[^ ]+" | head -1)
    if ! echo "$url" | grep -qiE "(github\.com|raw\.githubusercontent\.com)"; then
      RISK_LEVEL="yellow"; RISK_REASONS+=("Task contains external URL: $url")
    fi
  fi

  # Yellow: side-effect operations
  for kw in "write file" "send message" "modify config" "push" "commit"; do
    if echo "$content" | grep -qi "$kw"; then
      RISK_LEVEL="yellow"; RISK_REASONS+=("Task contains side-effect keyword '$kw'"); break
    fi
  done
}

update_sender_state() {
  local from="$1"
  python3 - <<EOF
import json, time, os
from datetime import datetime, timezone
f = '$STATE_FILE'
state = json.load(open(f)) if os.path.exists(f) else {'senderHistory': {}, 'pendingTasks': []}
now = time.time()
now_iso = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
if '$from' not in state['senderHistory']:
    state['senderHistory']['$from'] = {'firstSeen': now_iso, 'lastActive': now_iso, 'taskCount': 0, 'tasks_last_1h': []}
h = state['senderHistory']['$from']
h['lastActive'] = now_iso
h['taskCount'] = h.get('taskCount', 0) + 1
tasks_1h = [t for t in h.get('tasks_last_1h', []) if now - t < 3600]
tasks_1h.append(now)
h['tasks_last_1h'] = tasks_1h
with open(f, 'w') as fh:
    json.dump(state, fh, indent=2)
EOF
}

add_pending_task() {
  local from="$1" msg_file="$2" risk_level="$3" risk_reason="$4"
  python3 -c "
import json, os, sys
from datetime import datetime, timezone
from_arg = sys.argv[1]
msg_file_arg = sys.argv[2]
risk_level_arg = sys.argv[3]
risk_reason_arg = sys.argv[4]
f = os.environ.get('AGENT_BUS_STATE_FILE', '$STATE_FILE')
state = json.load(open(f)) if os.path.exists(f) else {'senderHistory': {}, 'pendingTasks': []}
state.setdefault('pendingTasks', []).append({
    'id': os.path.basename(msg_file_arg),
    'from': from_arg,
    'riskLevel': risk_level_arg,
    'riskReason': risk_reason_arg,
    'msgFile': msg_file_arg,
    'receivedAt': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'status': 'pending_confirmation'
})
with open(f, 'w') as fh:
    json.dump(state, fh, indent=2)
" "$from" "$msg_file" "$risk_level" "$risk_reason"
}

# --------------------------------------------------------------------------
# Command: setup-repo (first agent creating a new Bus)
# --------------------------------------------------------------------------
cmd_setup_repo() {
  local owner_id=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --owner) owner_id="${2:-}"; shift 2 ;;
      *) die "Unknown argument: $1" ;;
    esac
  done
  [[ -z "$owner_id" ]] && die "Usage: agent-bus.sh setup-repo --owner <agent-id>"

  [[ ! -d "$REPO_DIR/.git" ]] && die "Not a git repository: $REPO_DIR. Please cd into the repo root first."

  log_info "Initializing Agent Bus repo structure for owner: $owner_id"

  mkdir -p "$REPO_DIR/shared"
  mkdir -p "$REPO_DIR/inbox/$owner_id"
  mkdir -p "$REPO_DIR/requests"
  mkdir -p "$REPO_DIR/responses"

  if [[ ! -f "$REPO_DIR/shared/agents.json" ]]; then
    cat > "$REPO_DIR/shared/agents.json" <<EOF
{
  "version": "2",
  "agents": [
    {
      "id": "$owner_id",
      "name": "$owner_id",
      "description": "Bus creator",
      "joinedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    }
  ],
  "pairs": []
}
EOF
    log_info "Created shared/agents.json"
  else
    log_info "shared/agents.json already exists, skipping"
  fi

  if [[ ! -f "$REPO_DIR/shared/MEMORY-PUBLIC.md" ]]; then
    cat > "$REPO_DIR/shared/MEMORY-PUBLIC.md" <<'EOF'
# MEMORY-PUBLIC.md — Agent Bus Shared Memory

This file records information that all agents on this Bus need to know.
All agents can read; writes require the Bus owner's confirmation.

---

## Connected Agents

(Auto-populated during setup; update manually as agents join)

## Shared Conventions

(Record cross-agent collaboration rules here)
EOF
    log_info "Created shared/MEMORY-PUBLIC.md"
  fi

  # Copy PROTOCOL.md from skill directory (same dir as this script)
  if [[ ! -f "$REPO_DIR/shared/PROTOCOL.md" ]]; then
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local proto_src="$script_dir/PROTOCOL.md"
    if [[ -f "$proto_src" ]]; then
      cp "$proto_src" "$REPO_DIR/shared/PROTOCOL.md"
      log_info "Copied shared/PROTOCOL.md from skill directory"
    else
      cat > "$REPO_DIR/shared/PROTOCOL.md" <<'EOF'
# Agent Bus Protocol v0.4

See the agent-bus SKILL.md for the full protocol documentation.
EOF
      log_info "Created shared/PROTOCOL.md (minimal stub)"
    fi
  fi

  touch "$REPO_DIR/inbox/$owner_id/.gitkeep"
  touch "$REPO_DIR/requests/.gitkeep"
  touch "$REPO_DIR/responses/.gitkeep"

  if [[ ! -f "$REPO_DIR/README.md" ]]; then
    cat > "$REPO_DIR/README.md" <<EOF
# Agent Bus

This is a private Agent communication bus repository.
Agents communicate by reading/writing files via the shared inbox structure.

**Do not edit files directly. All operations must go through \`agent-bus.sh\`.**

Bus Owner: $owner_id
Created:   $(date -u +%Y-%m-%d)
EOF
    log_info "Created README.md"
  fi

  cd "$REPO_DIR"
  git add .
  git commit -m "chore: init agent-bus repo structure, owner=$owner_id" --quiet
  git push origin main --quiet

  echo "========================================"
  echo "Agent Bus repo initialized."
  echo ""
  echo "  Owner:     $owner_id"
  echo "  Structure:"
  echo "    shared/     — protocol docs, agent registry"
  echo "    inbox/      — per-agent inboxes"
  echo "    requests/   — pair requests"
  echo "    responses/  — pair responses"
  echo ""
  echo "Next step: run ./agent-bus.sh init $owner_id"
  echo "========================================"
}

# --------------------------------------------------------------------------
# Feature check: verify that a pair has a specific feature enabled
# Returns 0=enabled, 1=not enabled
# --------------------------------------------------------------------------
check_pair_feature() {
  local a="$1" b="$2" feature="$3"
  python3 - <<EOF
import json, sys
try:
    with open('$REPO_DIR/shared/agents.json') as f:
        data = json.load(f)
    for p in data.get('pairs', []):
        if (p['a'] == '$a' and p['b'] == '$b') or (p['a'] == '$b' and p['b'] == '$a'):
            if '$feature' in p.get('features', []):
                print('yes'); sys.exit(0)
    print('no')
except:
    print('no')
EOF
}

# --------------------------------------------------------------------------
# Command: init
# --------------------------------------------------------------------------
cmd_init() {
  local my_id="${1:-}"
  [[ -z "$my_id" ]] && die "Usage: agent-bus.sh init <agent-id>"

  mkdir -p "$(dirname "$ACL_FILE")"
  echo "$my_id" > "$MY_ID_FILE"
  log_info "Agent ID set: $my_id"

  if [[ ! -f "$ACL_FILE" ]]; then
    cat > "$ACL_FILE" <<EOF
{
  "myId": "$my_id",
  "lastConfirmedAt": "$(ts_now)",
  "allowReceiveFrom": [],
  "allowSendTo": [],
  "confirmedBy": "",
  "pendingChanges": []
}
EOF
    log_info "ACL file created: $ACL_FILE"
    log_warn "ACL allowlists are empty. Pair with another agent to begin communicating."
  fi

  if [[ ! -f "$STATE_FILE" ]]; then
    echo '{"senderHistory": {}, "pendingTasks": []}' > "$STATE_FILE"
    log_info "State file created: $STATE_FILE"
  fi

  if [[ ! -f "$USAGE_FILE" ]]; then
    echo '{"sent": {}, "received": {}}' > "$USAGE_FILE"
    log_info "Usage file created: $USAGE_FILE"
  fi
}

# --------------------------------------------------------------------------
# Command: send
# --------------------------------------------------------------------------
cmd_send() {
  # Usage: send <to> <type> <content> [--seq N] [--ack-required] [--part X/Y]
  local _all_args=("$@")
  local to="${1:-}" type="${2:-}" content="${3:-}"
  [[ -z "$to" || -z "$type" || -z "$content" ]] && \
    die "Usage: agent-bus.sh send <to> <type> <content> [--seq N] [--ack-required] [--part X/Y]  (type: task | reply | sync | notify | memory-sync)"

  # Parse optional flags from full arg list
  local seq_num="" ack_required="false" part_tag=""
  local _prev=""
  local _extra_args=()
  if [[ ${#_all_args[@]} -gt 3 ]]; then
    _extra_args=("${_all_args[@]:3}")
  fi
  for _fv in "${_extra_args[@]+"${_extra_args[@]}"}"; do
    [[ "$_fv" == "--ack-required" ]] && ack_required="true" || true
    [[ "$_prev" == "--seq" ]] && seq_num="$_fv" || true
    [[ "$_prev" == "--part" ]] && part_tag="$_fv" || true
    _prev="$_fv"
  done

  local my_id
  my_id=$(get_my_id)

  check_length "$content"
  scan_company_keywords "$content"
  scan_injection "$content"

  check_pair "$my_id" "$to" "$type" || die "Pair validation failed. Message rejected."

  # memory-sync requires the feature to be enabled on the pair
  if [[ "$type" == "memory-sync" ]]; then
    local feat_enabled
    feat_enabled=$(check_pair_feature "$my_id" "$to" "memory-sync")
    if [[ "$feat_enabled" != "yes" ]]; then
      die "Cannot send memory-sync: feature 'memory-sync' is not enabled for the pair '$my_id'↔'$to'. Re-pair with --features memory-sync to enable."
    fi
  fi

  # Auto-generate seq if not provided: use outbox count + 1
  if [[ -z "$seq_num" ]]; then
    local outbox_dir_pre="$REPO_DIR/outbox/${my_id}"
    local existing_count=0
    if [[ -d "$outbox_dir_pre" ]]; then
      existing_count=$(ls "$outbox_dir_pre" 2>/dev/null | grep -- "-to-${to}-" | wc -l | tr -d ' ')
    fi
    seq_num=$((existing_count + 1))
  fi

  local ts_slug
  ts_slug=$(make_ts_slug)
  mkdir -p "$REPO_DIR/inbox/${to}"
  local msg_file="$REPO_DIR/inbox/${to}/${ts_slug}-${my_id}-${type}.md"

  # Build optional header lines
  local part_header="" ack_header="" seq_header=""
  seq_header="seq: ${seq_num}"
  ack_header="ack_required: ${ack_required}"
  [[ -n "$part_tag" ]] && part_header="part: ${part_tag}"

  # Append part suffix to content if this is a multi-part message
  local content_with_suffix="$content"
  if [[ -n "$part_tag" ]]; then
    local cur_part total_parts
    cur_part=$(echo "$part_tag" | cut -d/ -f1)
    total_parts=$(echo "$part_tag" | cut -d/ -f2)
    if [[ "$cur_part" == "$total_parts" ]]; then
      content_with_suffix="${content}

---
All ${total_parts} parts sent. Please read all parts and reply."
    fi
  fi

  cat > "$msg_file" <<EOF
type: ${type}
from: ${my_id}
to: ${to}
subject: ""
timestamp: $(ts_now)
status: unread
${seq_header}
${ack_header}
${part_header}
pair_ref:
---

${content_with_suffix}
EOF

  cd "$REPO_DIR"
  git add "$msg_file"
  git commit -m "msg: ${my_id}→${to} [${type}] seq=${seq_num} @ ${ts_slug}" --quiet
  git push origin main --quiet

  # O3: record a copy in local outbox for audit/history
  local outbox_dir="$REPO_DIR/outbox/${my_id}"
  mkdir -p "$outbox_dir"
  local outbox_file="$outbox_dir/${ts_slug}-to-${to}-${type}.md"
  cat > "$outbox_file" <<OUTEOF
type: ${type}
from: ${my_id}
to: ${to}
subject: ""
timestamp: $(ts_now)
status: sent
${seq_header}
${ack_header}
${part_header}
pair_ref:
---

${content_with_suffix}
OUTEOF

  log_info "Message sent: $(basename "$msg_file")"
  echo "$msg_file"
}

# --------------------------------------------------------------------------
# Command: check (health check)
# --------------------------------------------------------------------------
cmd_check() {
  local issues=0

  echo "=== Agent Bus Health Check ==="
  echo ""

  # 1. Check agent ID file
  if [[ -f "$MY_ID_FILE" ]]; then
    local my_id
    my_id=$(cat "$MY_ID_FILE")
    echo "✅ Agent ID: $my_id"
  else
    echo "❌ Agent ID not found (expected: $MY_ID_FILE)"
    echo "   Run: agent-bus.sh init <agent-id>"
    issues=$((issues + 1))
  fi

  # 2. Check agents.json and list paired agents
  local agents_file="$REPO_DIR/shared/agents.json"
  if [[ -f "$agents_file" ]]; then
    local pair_count agent_count
    pair_count=$(python3 -c "
import json
data = json.load(open('$agents_file'))
pairs = data.get('pairs', [])
print(len(pairs))
" 2>/dev/null || echo "0")
    agent_count=$(python3 -c "
import json
data = json.load(open('$agents_file'))
agents = data.get('agents', [])
print(len(agents))
" 2>/dev/null || echo "0")
    echo "✅ agents.json found: $agent_count agent(s), $pair_count pair(s)"
    if [[ "$pair_count" -gt 0 ]]; then
      python3 -c "
import json
data = json.load(open('$agents_file'))
for p in data.get('pairs', []):
    a = p.get('a','?')
    b = p.get('b','?')
    status = p.get('status','?')
    print(f'   Pair: {a} ↔ {b} [{status}]')
" 2>/dev/null || true
    fi
  else
    echo "⚠️  agents.json not found ($agents_file)"
    echo "   No pairs configured yet."
    issues=$((issues + 1))
  fi

  # 3. Check inbox for unread messages
  local unread_count=0
  if [[ -f "$MY_ID_FILE" ]]; then
    local my_id
    my_id=$(cat "$MY_ID_FILE")
    local inbox_dir="$REPO_DIR/inbox/${my_id}"
    if [[ -d "$inbox_dir" ]]; then
      unread_count=$(grep -rl "^status: unread$" "$inbox_dir" 2>/dev/null || true | wc -l | tr -d ' ')
    fi
  fi
  if [[ "$unread_count" -gt 0 ]]; then
    echo "📬 Inbox: $unread_count unread message(s)"
  else
    echo "✅ Inbox: no unread messages"
  fi

  # 4. Check git remote reachability
  echo ""
  echo "Checking git remote..."
  if cd "$REPO_DIR" && git ls-remote --exit-code origin HEAD &>/dev/null; then
    local remote_url
    remote_url=$(git remote get-url origin 2>/dev/null || echo "unknown")
    echo "✅ Git remote reachable: $remote_url"
  else
    echo "❌ Git remote unreachable (check network / credentials)"
    issues=$((issues + 1))
  fi

  # 5. Overall status
  echo ""
  if [[ "$issues" -eq 0 ]]; then
    echo "✅ Agent Bus healthy"
  else
    echo "⚠️  Issues detected ($issues issue(s) found)"
  fi
}

# --------------------------------------------------------------------------
# Command: read
# --------------------------------------------------------------------------
cmd_read() {
  local my_id
  my_id=$(get_my_id)

  check_pending_pairs
  check_revoke_notifications

  local inbox_dir="$REPO_DIR/inbox/${my_id}"
  if [[ ! -d "$inbox_dir" ]]; then
    log_info "No unread messages."
    return 0
  fi

  local found=0
  for f in "$inbox_dir"/*.md; do
    [[ -f "$f" ]] || continue

    local from type status
    from=$(grep   "^from:"   "$f" | awk '{print $2}' | tr -d '[:space:]')
    type=$(grep   "^type:"   "$f" | awk '{print $2}' | tr -d '[:space:]')
    status=$(grep "^status:" "$f" | awk '{print $2}' | tr -d '[:space:]')

    [[ "$status" != "unread" ]] && continue

    # Independent pair validation (do not trust sender's self-report)
    if ! check_pair "$from" "$my_id" "$type" 2>/dev/null; then
      log_warn "Pair validation failed for message from '$from'. Rejected: $(basename "$f")"
      log_warn "Notify your owner to investigate."
      sed -i 's/^status: unread$/status: rejected/' "$f"
      # B12: write reject_reason
      if ! grep -q "^reject_reason:" "$f" 2>/dev/null; then
        sed -i "/^status: rejected/a reject_reason: acl-denied (no valid pair relationship)" "$f"
      fi
      continue
    fi

    # memory-sync: verify feature is enabled before accepting
    if [[ "$type" == "memory-sync" ]]; then
      local feat_ok
      feat_ok=$(check_pair_feature "$from" "$my_id" "memory-sync")
      if [[ "$feat_ok" != "yes" ]]; then
        log_warn "Received memory-sync from '$from' but feature is not enabled on this pair. Rejected: $(basename "$f")"
        log_warn "Notify your owner: '$from' attempted memory-sync without authorization."
        sed -i 's/^status: unread$/status: rejected/' "$f"
        # B12: write reject_reason
        if ! grep -q "^reject_reason:" "$f" 2>/dev/null; then
          sed -i "/^status: rejected/a reject_reason: acl-denied (memory-sync feature not enabled)" "$f"
        fi
        cd "$REPO_DIR" && git add "$f" && git commit -m "msg-rejected (feature not enabled): $(basename $f)" --quiet && git push origin main --quiet
        continue
      fi
      # memory-sync: display content and let the agent decide how to update MEMORY.md
      local content
      content=$(awk '/^---$/{found++; next} found>=1{print}' "$f")
      echo "========================================"
      echo "[MEMORY-SYNC] $(basename "$f")"
      echo "  From: $from"
      echo "  Note: This is a memory-sync message. Review and decide whether to update your MEMORY.md."
      echo "----------------------------------------"
      echo "$content"
      echo ""
      found=1
      update_sender_state "$from"
      continue
    fi

    local content
    content=$(awk '/^---$/{found++; next} found>=1{print}' "$f")

    if [[ "$type" == "task" ]]; then
      assess_risk "$from" "$content" "$type"

      if [[ "$RISK_LEVEL" == "red" ]]; then
        local red_reason_str
        red_reason_str=$(IFS="; "; echo "${RISK_REASONS[*]}")
        add_pending_task "$from" "$f" "red" "$red_reason_str"
        sed -i 's/^status: unread$/status: pending/' "$f"
        cd "$REPO_DIR" && git add "$f" && git commit -m "msg-pending (red): $(basename $f)" --quiet && git push origin main --quiet
        # Notify owner for confirmation — do NOT auto-reject
        local msg_preview
        msg_preview=$(echo "$content" | head -c 100)
        echo ""
        echo "🚨  Agent Bus high-risk message pending confirmation"
        echo "From: $from"
        echo "Risk level: red"
        echo "Risk reason: $red_reason_str"
        echo "Message preview: ${msg_preview}"
        echo ""
        echo "Please confirm before deciding whether to execute:"
        echo "  approve: bash agent-bus.sh approve $(basename "$f")"
        echo "  reject:  bash agent-bus.sh reject  $(basename "$f")"
        echo ""
        found=1
        # B10: do NOT call update_sender_state here — only update on approve
        continue
      fi

      if [[ "$RISK_LEVEL" == "yellow" ]]; then
        local reason_str
        reason_str=$(IFS="; "; echo "${RISK_REASONS[*]}")
        add_pending_task "$from" "$f" "yellow" "$reason_str"
        sed -i 's/^status: unread$/status: pending/' "$f"
        cd "$REPO_DIR" && git add "$f" && git commit -m "msg-pending: $(basename $f)" --quiet && git push origin main --quiet
        # O2: structured pending notification
        local msg_preview
        msg_preview=$(echo "$content" | head -c 100)
        echo ""
        echo "⚠️  Agent Bus pending approval message"
        echo "From: $from"
        echo "Risk level: yellow"
        echo "Risk reason: $reason_str"
        echo "Message preview: ${msg_preview}"
        echo ""
        echo "Approval commands:"
        echo "  approve: bash agent-bus.sh approve $(basename "$f")"
        echo "  reject:  bash agent-bus.sh reject  $(basename "$f")"
        echo ""
        found=1
        # B10: do NOT call update_sender_state here — only update on approve
        continue
      fi
    fi

    echo "========================================"
    echo "[$(echo "$type" | tr '[:lower:]' '[:upper:]')] $(basename "$f")"
    echo "  From: $from"
    echo "----------------------------------------"
    echo "$content"
    echo ""
    found=1
    update_sender_state "$from"

    # O5: auto-ack — mark status: unread -> status: read after display, prevent duplicate polling
    sed -i 's/^status: unread$/status: read/' "$f"
    (cd "$REPO_DIR" && git add "$f" && git commit -m "msg-read (auto-ack): $(basename \"$f\")" --quiet && git push origin main --quiet) || true
  done

  if (( found == 0 )); then log_info "No unread messages."; fi

  # Show summary of pending and rejected messages
  local my_id_for_scan
  my_id_for_scan=$(get_my_id)
  local inbox_dir_scan="$REPO_DIR/inbox/${my_id_for_scan}"
  if [[ -d "$inbox_dir_scan" ]]; then
    local pending_count=0 rejected_count=0
    for f in "$inbox_dir_scan"/*.md; do
      [[ -f "$f" ]] || continue
      local s
      s=$(grep "^status:" "$f" | awk '{print $2}' | tr -d '[:space:]')
      [[ "$s" == "pending" ]] && (( pending_count++ )) || true
      [[ "$s" == "rejected" ]] && (( rejected_count++ )) || true
    done
    if (( pending_count > 0 )); then
      echo ""
      echo "📋 Pending: ${pending_count} message(s) awaiting confirmation (run 'agent-bus.sh pending' for details)"
    fi
    if (( rejected_count > 0 )); then
      echo ""
      echo "🚫 Rejected: ${rejected_count} message(s) rejected (run 'agent-bus.sh rejected' to view)"
    fi
  fi
}

# --------------------------------------------------------------------------
# Command: approve / reject (task confirmation)
# --------------------------------------------------------------------------
cmd_approve() {
  local msg_basename="${1:-}"
  [[ -z "$msg_basename" ]] && die "Usage: agent-bus.sh approve <message-filename>"
  local msg_file
  msg_file=$(find "$REPO_DIR/inbox" -name "$msg_basename" 2>/dev/null | head -1)
  [[ -z "$msg_file" ]] && die "Message file not found: $msg_basename"
  sed -i 's/^status: pending$/status: approved/' "$msg_file"
  # B10: extract sender from pending task and write senderHistory on approve
  local approved_from
  approved_from=$(grep "^from:" "$msg_file" 2>/dev/null | awk '{print $2}' | tr -d '[:space:]' || true)
  python3 - <<EOF
import json, os, time
from datetime import datetime, timezone
f = '$STATE_FILE'
state = json.load(open(f)) if os.path.exists(f) else {'senderHistory': {}, 'pendingTasks': []}
state.setdefault('senderHistory', {})
# Remove from pendingTasks
state['pendingTasks'] = [t for t in state.get('pendingTasks', []) if t.get('id') != '$msg_basename']
# Write senderHistory for the approved sender (B10 fix)
sender = '$approved_from'
if sender:
    now = time.time()
    now_iso = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    if sender not in state['senderHistory']:
        state['senderHistory'][sender] = {'firstSeen': now_iso, 'lastActive': now_iso, 'taskCount': 0, 'tasks_last_1h': []}
    h = state['senderHistory'][sender]
    h['lastActive'] = now_iso
    h['taskCount'] = h.get('taskCount', 0) + 1
    tasks_1h = [t for t in h.get('tasks_last_1h', []) if now - t < 3600]
    tasks_1h.append(now)
    h['tasks_last_1h'] = tasks_1h
with open(f, 'w') as fh:
    json.dump(state, fh, indent=2)
EOF
  cd "$REPO_DIR" && git add "$msg_file" && git commit -m "msg-approved: $msg_basename" --quiet && git push origin main --quiet
  log_info "Task approved: $msg_basename"
  cat "$msg_file"
}

cmd_reject() {
  local msg_basename="${1:-}" reject_reason="owner-rejected"
  # Support optional --reason flag
  shift || true
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --reason) reject_reason="${2:-owner-rejected}"; shift 2 ;;
      *) shift ;;
    esac
  done
  [[ -z "$msg_basename" ]] && die "Usage: agent-bus.sh reject <message-filename> [--reason <reason>]"
  local msg_file
  msg_file=$(find "$REPO_DIR/inbox" -name "$msg_basename" 2>/dev/null | head -1)
  [[ -z "$msg_file" ]] && die "Message file not found: $msg_basename"
  sed -i 's/^status: pending$/status: rejected/; s/^status: unread$/status: rejected/' "$msg_file"
  # B12: append reject_reason to the message file
  if ! grep -q "^reject_reason:" "$msg_file" 2>/dev/null; then
    sed -i "/^status: rejected/a reject_reason: ${reject_reason}" "$msg_file"
  fi
  python3 - <<EOF
import json, os
f = '$STATE_FILE'
if os.path.exists(f):
    state = json.load(open(f))
    state['pendingTasks'] = [t for t in state.get('pendingTasks', []) if t.get('id') != '$msg_basename']
    with open(f, 'w') as fh:
        json.dump(state, fh, indent=2)
EOF
  cd "$REPO_DIR" && git add "$msg_file" && git commit -m "msg-rejected: $msg_basename" --quiet && git push origin main --quiet
  log_info "Task rejected: $msg_basename (reason: $reject_reason)"
}

# --------------------------------------------------------------------------
# Command: pending
# --------------------------------------------------------------------------
cmd_pending() {
  [[ ! -f "$STATE_FILE" ]] && { log_info "No pending tasks."; return 0; }
  python3 - <<EOF
import json
with open('$STATE_FILE') as f:
    state = json.load(f)
tasks = state.get('pendingTasks', [])
if not tasks:
    print('[INFO]  No pending tasks.')
else:
    print(f'{len(tasks)} pending task(s):')
    for t in tasks:
        print(f"  [{t['riskLevel'].upper()}] {t['id']}")
        print(f"    From:   {t['from']}")
        print(f"    Reason: {t['riskReason']}")
        print(f"    Time:   {t['receivedAt']}")
        print()
EOF
}

# --------------------------------------------------------------------------
# Command: rejected
# --------------------------------------------------------------------------
cmd_rejected() {
  local my_id
  my_id=$(get_my_id)
  local inbox_dir="$REPO_DIR/inbox/${my_id}"
  if [[ ! -d "$inbox_dir" ]]; then
    log_info "No rejected messages."
    return 0
  fi

  local count=0
  for f in "$inbox_dir"/*.md; do
    [[ -f "$f" ]] || continue
    local status
    status=$(grep "^status:" "$f" | awk '{print $2}' | tr -d '[:space:]')
    [[ "$status" != "rejected" ]] && continue

    local from reason ts
    from=$(grep   "^from:"          "$f" 2>/dev/null | awk '{print $2}' | tr -d '[:space:]' || true)
    reason=$(grep "^reject_reason:" "$f" 2>/dev/null | cut -d' ' -f2- || true)
    ts=$(grep     "^timestamp:"     "$f" 2>/dev/null | awk '{print $2}' | tr -d '[:space:]' || true)

    if (( count == 0 )); then
      echo "========================================"
      echo "Rejected messages:"
      echo "========================================"
    fi
    echo "  [REJECTED] $(basename "$f")"
    echo "    From:   ${from:-unknown}"
    echo "    Reason: ${reason:-unknown}"
    echo "    Time:   ${ts:-unknown}"
    echo ""
    (( count++ )) || true
  done

  if (( count == 0 )); then
    log_info "No rejected messages."
  else
    echo "Total: ${count} rejected message(s)."
  fi
}

# --------------------------------------------------------------------------
# Command: ack
# --------------------------------------------------------------------------
cmd_ack() {
  local msg_file="${1:-}"
  [[ -z "$msg_file" ]] && die "Usage: agent-bus.sh ack <message-file-path>"
  [[ -f "$msg_file" ]] || die "File not found: $msg_file"
  sed -i 's/^status: unread$/status: read/; s/^status: approved$/status: read/' "$msg_file"
  cd "$REPO_DIR" && git add "$msg_file" && git commit -m "msg-acked: $(basename $msg_file)" --quiet && git push origin main --quiet
  log_info "Marked as read: $msg_file"
}

# --------------------------------------------------------------------------
# Command: sync-acl
# --------------------------------------------------------------------------
cmd_sync_acl() {
  local agents_file="$REPO_DIR/shared/agents.json"
  [[ -f "$agents_file" ]] || die "agents.json not found: $agents_file"
  [[ -f "$ACL_FILE" ]]    || die "ACL file not found. Run: agent-bus.sh init"

  local my_id
  my_id=$(get_my_id)

  python3 - <<EOF
import json
from datetime import datetime, timezone

with open('$agents_file') as f:
    data = json.load(f)

with open('$ACL_FILE') as f:
    acl = json.load(f)

my_id = '$my_id'
pairs = data.get('pairs', [])

added = 0
for pair in pairs:
    a, b = pair.get('a', ''), pair.get('b', '')
    # Determine the other side of the pair
    if a == my_id:
        other = b
    elif b == my_id:
        other = a
    else:
        continue  # This pair doesn't involve me

    changed = False
    if other not in acl.get('allowReceiveFrom', []):
        acl.setdefault('allowReceiveFrom', []).append(other)
        changed = True
    if other not in acl.get('allowSendTo', []):
        acl.setdefault('allowSendTo', []).append(other)
        changed = True
    if changed:
        added += 1

acl['lastConfirmedAt'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
with open('$ACL_FILE', 'w') as f:
    json.dump(acl, f, indent=2)

print(f'\u2705 ACL synced: {added} agent(s) added')
EOF
}

# --------------------------------------------------------------------------
# Commands: update-acl / check-acl / detect-changes
# --------------------------------------------------------------------------
cmd_check_acl() {
  local direction="${1:-}" agent_id="${2:-}"
  [[ -z "$direction" || -z "$agent_id" ]] && die "Usage: agent-bus.sh check-acl <allowReceiveFrom|allowSendTo> <agent-id>"
  if check_acl "$direction" "$agent_id"; then
    log_info "'$agent_id' is in $direction allowlist."; exit 0
  else
    log_warn "'$agent_id' is NOT in $direction allowlist."; exit 1
  fi
}

cmd_update_acl() {
  local direction="${1:-}" agent_id="${2:-}" action="${3:-add}"
  [[ -z "$direction" || -z "$agent_id" ]] && die "Usage: agent-bus.sh update-acl <allowReceiveFrom|allowSendTo> <agent-id> [add|remove]"
  python3 - <<EOF
import json
from datetime import datetime, timezone
with open('$ACL_FILE') as f:
    acl = json.load(f)
d, aid, act = '$direction', '$agent_id', '$action'
if d not in ('allowReceiveFrom', 'allowSendTo'):
    print(f'Invalid direction: {d}'); exit(1)
if act == 'add':
    if aid not in acl[d]:
        acl[d].append(aid); print(f'Added {aid} to {d}')
    else:
        print(f'{aid} already in {d}')
elif act == 'remove':
    if aid in acl[d]:
        acl[d].remove(aid); print(f'Removed {aid} from {d}')
    else:
        print(f'{aid} not found in {d}')
acl['lastConfirmedAt'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
with open('$ACL_FILE', 'w') as f:
    json.dump(acl, f, indent=2)
EOF
  log_info "ACL updated."
}

cmd_detect_changes() {
  cd "$REPO_DIR" || die "Cannot enter repo directory"
  git fetch origin main --quiet 2>/dev/null || { log_warn "git fetch failed, skipping change detection"; return 0; }
  local diff
  diff=$(git diff HEAD origin/main -- shared/agents.json 2>/dev/null || true)
  [[ -z "$diff" ]] && { log_info "No changes in agents.json"; return 0; }
  local added removed
  added=$(echo "$diff" | grep '^+' | grep '"id"' | grep -v '^+++' | sed 's/.*"id": *"\([^"]*\)".*/\1/')
  removed=$(echo "$diff" | grep '^-' | grep '"id"' | grep -v '^---' | sed 's/.*"id": *"\([^"]*\)".*/\1/')
  echo "agents.json has changed and has not been applied to local ACL."
  [[ -n "$added" ]]   && echo "  Added agents:   $added"
  [[ -n "$removed" ]] && echo "  Removed agents: $removed"
  echo "Confirm with your owner, then run update-acl."
  exit 1
}

# --------------------------------------------------------------------------
# Main entry point
# --------------------------------------------------------------------------
usage() {
  cat <<'EOF'
Usage: agent-bus.sh <command> [args]

Setup:
  setup-repo --owner <agent-id>                         Init repo structure (first agent on a new Bus)
  init <agent-id>                                       Init local identity and ACL/state files

Messaging:
  send <to> <type> <content>                            Send a message (with security + pair checks)
  read                                                  Read inbox (with pair check + risk assessment)
  ack <message-file-path>                               Mark a message as read
  pending                                               List all pending (awaiting confirmation) tasks
  rejected                                              List all rejected messages
  approve <message-filename>                            Approve a pending task (after owner confirmation)
  reject  <message-filename>                            Reject a pending task

Pair management:
  pair-request --with <agent-id> --reason <reason> [--mode bidirectional|a→b|b→a] [--features memory-sync,...]
                                                        Send a pair request to another agent
  approve-pair <pair_req_filename> [--mode a→b|b→a] [--features memory-sync,...]
                                                        Approve a pair request (after owner confirmation)
  reject-pair  <pair_req_filename>                      Reject a pair request (after owner confirmation)
  revoke-pair  <other-agent-id>                         Revoke an existing pair (after owner instruction)

ACL management (requires owner confirmation):
  check-acl <direction> <agent-id>                      Check ACL allowlist
  update-acl <direction> <agent-id> [add|remove]        Update ACL
  sync-acl                                              Sync ACL from agents.json (auto-runs after approve-pair)
  detect-changes                                        Detect agents.json changes

Risk levels:
  RED    (auto-reject)    High-risk keywords / high-frequency anomaly / no pair relationship
  YELLOW (pending owner)  First-time sender / long-inactive / bulk ops / external URLs / side-effects
  GREEN  (auto-execute)   None of the above triggered

Pair modes:
  bidirectional   Both A and B can send tasks to each other (and reply)
  a→b             Only A can send tasks to B; B can only reply
  b→a             Only B can send tasks to A; A can only reply
EOF
}

case "${1:-}" in
  setup-repo)      cmd_setup_repo "${@:2}" ;;
  init)            cmd_init "${2:-}" ;;
  send)            cmd_send "${2:-}" "${3:-}" "${4:-}" "${@:5}" ;;
  check)           cmd_check ;;
  read)            cmd_read ;;
  ack)             cmd_ack "${2:-}" ;;
  pending)         cmd_pending ;;
  rejected)        cmd_rejected ;;
  approve)         cmd_approve "${2:-}" ;;
  reject)          cmd_reject "${2:-}" ;;
  pair-request)    cmd_pair_request "${@:2}" ;;
  approve-pair)    cmd_approve_pair "${@:2}" ;;
  reject-pair)     cmd_reject_pair "${2:-}" ;;
  revoke-pair)     cmd_revoke_pair "${2:-}" ;;
  check-acl)       cmd_check_acl "${2:-}" "${3:-}" ;;
  update-acl)      cmd_update_acl "${2:-}" "${3:-}" "${4:-add}" ;;
  sync-acl)        cmd_sync_acl ;;
  detect-changes)  cmd_detect_changes ;;
  *)               usage ;;
esac
