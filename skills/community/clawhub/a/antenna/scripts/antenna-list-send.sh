#!/usr/bin/env bash
# Local Distribution List fan-out with optional visible-recipient metadata.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
LISTS_FILE="$SKILL_DIR/antenna-lists.json"
PEERS_FILE="$SKILL_DIR/antenna-peers.json"
CONFIG_FILE="$SKILL_DIR/antenna-config.json"
SENDER="$SCRIPT_DIR/antenna-send.sh"
META="$SKILL_DIR/lib/antenna-list-meta.py"
source "$SKILL_DIR/lib/peers.sh"
source "$SKILL_DIR/lib/antenna-signature.sh"
die() { printf 'Error: %s\n' "$1" >&2; exit 1; }

SHOW=false READ_STDIN=false
MEMBERS=() SESSIONS=() OPTIONS=() POSITIONAL=()
[[ $# -ge 1 ]] || die "Usage: antenna send @alias ..."
ALIAS_REF="$1"; shift
[[ "$ALIAS_REF" =~ ^@[a-z0-9][a-z0-9._-]{0,63}$ ]] || die "Invalid distribution-list alias"
ALIAS="${ALIAS_REF#@}"; LABEL="@$ALIAS"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --show-recipients) SHOW=true; shift ;;
    --session) die "Distribution List sessions belong in antenna-lists.json; command-level --session is not supported" ;;
    --subject|--user|--reply-to) [[ $# -ge 2 ]] || die "$1 requires a value"; OPTIONS+=("$1" "$2"); shift 2 ;;
    --dry-run|--json) OPTIONS+=("$1"); shift ;;
    --stdin) READ_STDIN=true; shift ;;
    -*) die "Unknown option: $1" ;;
    *) POSITIONAL+=("$1"); shift ;;
  esac
done
[[ "$READ_STDIN" == false || ${#POSITIONAL[@]} -eq 0 ]] || die "Do not combine --stdin with a positional message"
[[ "$READ_STDIN" == true || ${#POSITIONAL[@]} -gt 0 ]] || die "No message provided. Use positional arg or --stdin."

[[ -f "$LISTS_FILE" && ! -L "$LISTS_FILE" ]] || die "Distribution-list file must be a regular non-symlink file"
jq -e 'type=="object" and length<=100 and all(to_entries[];
  (.key|test("^[a-z0-9][a-z0-9._-]{0,63}$")) and
  (.value|type)=="array" and (.value|length)>0 and (.value|length)<=100 and
  all(.value[];
    type=="object" and
    ((keys - ["peer", "session"])|length)==0 and
    (.peer|type)=="string" and (.peer|test("^[a-z0-9][a-z0-9._-]{0,63}$")) and
    ((has("session")|not) or
      ((.session|type)=="string" and
       (.session|length)<=128 and
       (.session|test("^agent:[A-Za-z0-9][A-Za-z0-9._-]{0,63}:[A-Za-z0-9][A-Za-z0-9._-]{0,127}$"))))
  ) and
  (([.value[].peer]|unique|length)==(.value|length)))' \
  "$LISTS_FILE" >/dev/null 2>&1 || die "Malformed or oversized antenna-lists.json"
jq -e --arg alias "$ALIAS" 'has($alias)' "$LISTS_FILE" >/dev/null || die "Unknown distribution list: @$ALIAS"
while IFS=$'\t' read -r member session; do
  MEMBERS+=("$member")
  SESSIONS+=("$session")
done < <(jq -r --arg alias "$ALIAS" '.[$alias] | sort_by(.peer)[] | [.peer, (.session // "")] | @tsv' "$LISTS_FILE")

SELF_ID=$(peers_single_self_id) || die "Expected exactly one configured self peer"
VALID=() NEED_ED=false NEED_LEGACY=false
for i in "${!MEMBERS[@]}"; do
  member="${MEMBERS[$i]}"
  if [[ "$member" == "$SELF_ID" ]]; then
    die "Distribution list $LABEL contains self peer '$member'"
  fi
  reason=""
  peers_exists "$member" || reason="unknown peer"
  if [[ -z "$reason" ]] && ! jq -e --arg peer "$member" '(.allowed_outbound_peers|type)=="array" and all(.allowed_outbound_peers[];type=="string") and (.allowed_outbound_peers|index($peer)!=null)' "$CONFIG_FILE" >/dev/null 2>&1; then reason="not outbound-allowed"; fi
  if [[ -z "$reason" ]]; then url=$(peers_get "$member" url); validate_peer_url "$url" "$(peers_get "$member" allow_http)" >/dev/null 2>&1 || reason="invalid URL"; fi
  if [[ -z "$reason" ]]; then token=$(peers_get "$member" token_file); [[ -n "$token" && "$token" != /* ]] && token="$SKILL_DIR/$token"; [[ -f "$token" && -r "$token" ]] || reason="missing token"; fi
  if [[ -z "$reason" ]]; then mode=$(peers_get "$member" auth_mode); case "$mode" in ed25519-v1) NEED_ED=true;; plaintext-legacy) NEED_LEGACY=true;; *) reason="unsupported auth mode";; esac; fi
  if [[ -n "$reason" ]]; then
    die "Distribution list $LABEL contains unavailable peer '$member' ($reason)"
  fi
  VALID+=("$member")
done
MEMBERS=("${VALID[@]}"); [[ ${#MEMBERS[@]} -gt 0 ]] || die "No locally usable recipients remain"
if [[ "$NEED_ED" == true ]]; then key=$(peers_get "$SELF_ID" signing_private_key_file); [[ -n "$key" && "$key" != /* ]] && key="$SKILL_DIR/$key"; signature_private_key_ok "$key" || die "Self Ed25519 credential is missing or unsafe"; fi
if [[ "$NEED_LEGACY" == true ]]; then key=$(peers_get "$SELF_ID" peer_secret_file); [[ -n "$key" && "$key" != /* ]] && key="$SKILL_DIR/$key"; legacy_secret_file_ok "$key" || die "Self legacy credential is missing or unsafe"; fi

BODY="" PREFIXED="" RESULTS="" OUT="" ERR="" SEND_STDIN=false
trap 'rm -f "$BODY" "$PREFIXED" "$RESULTS" "$OUT" "$ERR"' EXIT
if [[ "$READ_STDIN" == true || "$SHOW" == true ]]; then
  BODY=$(mktemp "${TMPDIR:-/tmp}/antenna-list-body.XXXXXX") || die "Could not stage body"; chmod 0600 "$BODY"; SEND_STDIN=true
  if [[ "$READ_STDIN" == true ]]; then cat >"$BODY"; else printf '%s' "${POSITIONAL[*]}" >"$BODY"; fi
fi
if [[ "$SHOW" == true ]]; then
  PREFIXED=$(mktemp "${TMPDIR:-/tmp}/antenna-list-prefixed.XXXXXX") || die "Could not stage metadata"; chmod 0600 "$PREFIXED"
  python3 "$META" prefix "$ALIAS" "$(IFS=,; echo "${MEMBERS[*]}")" "$BODY" "$PREFIXED" || exit 1
  rm -f "$BODY"; BODY="$PREFIXED"; PREFIXED=""
fi

RESULTS=$(mktemp "${TMPDIR:-/tmp}/antenna-list-results.XXXXXX"); OUT=$(mktemp "${TMPDIR:-/tmp}/antenna-list-out.XXXXXX"); ERR=$(mktemp "${TMPDIR:-/tmp}/antenna-list-err.XXXXXX")
chmod 0600 "$RESULTS" "$OUT" "$ERR"
overall=0
for i in "${!MEMBERS[@]}"; do
  member="${MEMBERS[$i]}"
  session="${SESSIONS[$i]}"
  member_options=("${OPTIONS[@]}")
  [[ -z "$session" ]] || member_options+=(--session "$session")
  set +e
  if [[ "$SEND_STDIN" == true ]]; then bash "$SENDER" "$member" "${member_options[@]}" --stdin <"$BODY" >"$OUT" 2>"$ERR"; else bash "$SENDER" "$member" "${member_options[@]}" "${POSITIONAL[@]}" >"$OUT" 2>"$ERR"; fi
  rc=$?; set -e; [[ ! -s "$ERR" ]] || cat "$ERR" >&2; [[ $rc -eq 0 ]] || overall=1
  if jq -e . "$OUT" >/dev/null 2>&1; then jq -n --arg peer "$member" --argjson rc "$rc" --slurpfile sender "$OUT" '{peer:$peer,ok:($rc==0),exit_code:$rc,sender:$sender[0]}' >>"$RESULTS"; else jq -n --arg peer "$member" --argjson rc "$rc" --rawfile output "$OUT" '{peer:$peer,ok:($rc==0),exit_code:$rc,sender_output:$output}' >>"$RESULTS"; fi
done
jq -s --arg label "$LABEL" --arg alias "$ALIAS_REF" '{alias:$alias,list:$label,total:length,succeeded:map(select(.ok))|length,failed:map(select(.ok|not))|length,results:.}' "$RESULTS"
exit "$overall"
