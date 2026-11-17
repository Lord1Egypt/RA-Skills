#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
ROUTES_FILE="${ANTENNA_PUBLIC_GROUPS_FILE:-$SKILL_DIR/antenna-public-groups.json}"
PEERS_FILE="${ANTENNA_PEERS_FILE:-$SKILL_DIR/antenna-peers.json}"
SEND_SCRIPT="$SKILL_DIR/scripts/antenna-send.sh"
source "$SKILL_DIR/lib/antenna-signature.sh"

die() { printf 'Error: %s\n' "$1" >&2; exit "${2:-1}"; }

valid_alias() { [[ "$1" =~ ^[a-z0-9][a-z0-9._-]{0,63}$ ]]; }

validate_route_file() {
  local file="$1" allow_empty="${2:-false}"
  [[ -f "$file" && ! -L "$file" ]] || die "Route file must be a regular file: $file"
  jq -e '
    type == "object" and
    all(to_entries[];
      (.key | test("^[a-z0-9][a-z0-9._-]{0,63}$")) and
      (.value | type == "object" and keys == ["group_id", "name", "relay_peer"]) and
      (.value.group_id | test("^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")) and
      (.value.name | type == "string" and length > 0 and length <= 128) and
      (.value.relay_peer | test("^[a-z0-9][a-z0-9._-]{0,63}$"))
    )
  ' "$file" >/dev/null 2>&1 || die "Invalid Public Group route file: $file"
  if [[ "$allow_empty" != "true" ]] && [[ "$(jq 'length' "$file")" -eq 0 ]]; then
    die "Public Group route file is empty: $file"
  fi
}

ensure_local_state() {
  local parent owner
  parent=$(dirname "$ROUTES_FILE")
  [[ -d "$parent" && ! -L "$parent" ]] || die "Route directory is missing or unsafe: $parent"
  if [[ -e "$ROUTES_FILE" || -L "$ROUTES_FILE" ]]; then
    validate_route_file "$ROUTES_FILE" true
    owner=$(stat -c '%u' "$ROUTES_FILE")
    [[ "$owner" -eq "$(id -u)" ]] || die "Local route file must be owned by the current user: $ROUTES_FILE"
    [[ "$(stat -c '%a' "$ROUTES_FILE")" == "600" ]] || die "Local route file must use mode 0600: $ROUTES_FILE"
  else
    umask 077
    printf '{}\n' >"$ROUTES_FILE"
    chmod 0600 "$ROUTES_FILE"
  fi
}

write_routes() {
  local candidate="$1" parent tmp
  validate_route_file "$candidate" true
  parent=$(dirname "$ROUTES_FILE")
  umask 077
  tmp=$(mktemp "$parent/.antenna-public-groups.XXXXXX")
  trap 'rm -f -- "${tmp:-}"' RETURN
  jq -S . "$candidate" >"$tmp"
  chmod 0600 "$tmp"
  mv -f -- "$tmp" "$ROUTES_FILE"
  trap - RETURN
}

require_relay_peer() {
  local relay="$1" signing_ref signing_path
  [[ -f "$PEERS_FILE" && ! -L "$PEERS_FILE" ]] || die "Antenna peers file is missing: $PEERS_FILE"
  jq -e --arg relay "$relay" '.[$relay].auth_mode == "ed25519-v1"' "$PEERS_FILE" >/dev/null 2>&1 \
    || die "Relay peer '$relay' must be configured with auth_mode ed25519-v1"
  signing_ref=$(jq -r --arg relay "$relay" '.[$relay].signing_public_key_file // empty' "$PEERS_FILE")
  [[ -n "$signing_ref" ]] || die "Relay peer '$relay' has no pinned Ed25519 signing public key"
  signing_path="$signing_ref"
  [[ "$signing_path" == /* ]] || signing_path="$SKILL_DIR/$signing_path"
  # Native plugin contact import stores its public pin in the private secrets
  # directory. Keep the same path/ownership/mode/type checks for both roots;
  # legacy registrations remain restricted to their original keys directory.
  if ! signature_public_key_ok "$signing_path" "$SKILL_DIR/keys"; then
    jq -e --arg relay "$relay" '.[$relay].transport_profile == "antenna-plugin-v2"' "$PEERS_FILE" >/dev/null 2>&1 \
      && signature_public_key_ok "$signing_path" "$SKILL_DIR/secrets" \
      || die "Relay peer '$relay' has an invalid or unsafe Ed25519 signing public key"
  fi
}

validate_relay_prerequisites() {
  local file="$1" relay
  while IFS= read -r relay; do require_relay_peer "$relay"; done < <(jq -r '.[].relay_peer' "$file" | sort -u)
}

list_groups() {
  ensure_local_state
  jq -r 'to_entries | sort_by(.key)[] | "@\(.key)\t\(.value.name)\t\(.value.group_id)\trelay=\(.value.relay_peer)"' "$ROUTES_FILE"
}

install_routes() {
  local input="${1:-}" alias_override="" candidate input_alias group_id existing_alias
  [[ -n "$input" ]] || die "Usage: antenna groups install <downloaded-route.json> [--alias <name>]"
  shift
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --alias) [[ $# -ge 2 ]] || die "--alias requires a value"; alias_override="${2#@}"; shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done
  validate_route_file "$input"
  [[ "$(jq 'length' "$input")" -eq 1 ]] || die "Install accepts exactly one downloaded route"
  validate_relay_prerequisites "$input"
  ensure_local_state
  input_alias=$(jq -r 'keys[0]' "$input")
  if [[ -n "$alias_override" ]]; then
    valid_alias "$alias_override" || die "Invalid local alias: $alias_override"
    input_alias="$alias_override"
  fi
  group_id=$(jq -r '.[keys[0]].group_id' "$input")
  existing_alias=$(jq -r --arg gid "$group_id" 'to_entries[] | select(.value.group_id == $gid) | .key' "$ROUTES_FILE")
  [[ -z "$existing_alias" ]] || die "Group is already installed as @$existing_alias; use refresh"
  jq -e --arg alias "$input_alias" 'has($alias) | not' "$ROUTES_FILE" >/dev/null \
    || die "Alias @$input_alias already exists"
  candidate=$(mktemp "${TMPDIR:-/tmp}/antenna-route-install.XXXXXX")
  trap 'rm -f -- "${candidate:-}"' RETURN
  jq --arg alias "$input_alias" --slurpfile incoming "$input" '. + {($alias): $incoming[0][$incoming[0] | keys[0]]}' "$ROUTES_FILE" >"$candidate"
  write_routes "$candidate"
  trap - RETURN
  rm -f -- "$candidate"
  printf 'Installed @%s\n' "$input_alias"
}

refresh_routes() {
  local input="${1:-}" candidate entry group_id local_alias
  [[ -n "$input" && $# -eq 1 ]] || die "Usage: antenna groups refresh <downloaded-route.json>"
  validate_route_file "$input"
  validate_relay_prerequisites "$input"
  ensure_local_state
  candidate=$(mktemp "${TMPDIR:-/tmp}/antenna-route-refresh.XXXXXX")
  cp -- "$ROUTES_FILE" "$candidate"
  trap 'rm -f -- "${candidate:-}"' RETURN
  while IFS= read -r entry; do
    group_id=$(jq -r '.value.group_id' <<<"$entry")
    local_alias=$(jq -r --arg gid "$group_id" 'to_entries[] | select(.value.group_id == $gid) | .key' "$candidate")
    [[ -n "$local_alias" ]] || die "Downloaded group $group_id is not installed"
    [[ "$(wc -l <<<"$local_alias")" -eq 1 ]] || die "Local route file contains duplicate group IDs"
    jq --arg alias "$local_alias" --argjson value "$(jq -c '.value' <<<"$entry")" '.[$alias] = $value' "$candidate" >"$candidate.next"
    mv -- "$candidate.next" "$candidate"
  done < <(jq -c 'to_entries[]' "$input")
  write_routes "$candidate"
  trap - RETURN
  rm -f -- "$candidate"
  printf 'Refreshed %s route(s)\n' "$(jq 'length' "$input")"
}

remove_route() {
  local alias="${1:-}" candidate
  [[ -n "$alias" && $# -eq 1 ]] || die "Usage: antenna groups remove <alias>"
  alias="${alias#@}"
  valid_alias "$alias" || die "Invalid local alias: $alias"
  ensure_local_state
  jq -e --arg alias "$alias" 'has($alias)' "$ROUTES_FILE" >/dev/null || die "Unknown Public Group: @$alias"
  candidate=$(mktemp "${TMPDIR:-/tmp}/antenna-route-remove.XXXXXX")
  trap 'rm -f -- "${candidate:-}"' RETURN
  jq --arg alias "$alias" 'del(.[$alias])' "$ROUTES_FILE" >"$candidate"
  write_routes "$candidate"
  trap - RETURN
  rm -f -- "$candidate"
  printf 'Removed @%s\n' "$alias"
}

send_group() {
  local alias="${1:-}" message="${2:-}" subject=""
  [[ -n "$alias" && -n "$message" ]] || die "Usage: antenna groups send <alias> <message> [--subject <text>]"
  shift 2
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --subject) [[ $# -ge 2 ]] || die "--subject requires a value"; subject="$2"; shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done
  alias="${alias#@}"
  ensure_local_state
  local route group_id relay body send_output send_rc failed
  route=$(jq -cer --arg alias "$alias" '.[$alias]' "$ROUTES_FILE") || die "Unknown Public Group: @$alias"
  group_id=$(jq -r '.group_id' <<<"$route")
  relay=$(jq -r '.relay_peer' <<<"$route")
  require_relay_peer "$relay"
  printf '%s\n' \
    'PUBLIC GROUP: ClawReef reads and relays this plaintext message. Do not send passwords, private keys, credentials, regulated data, or other sensitive plaintext.' >&2
  body=$(mktemp "${TMPDIR:-/tmp}/antenna-public-group.XXXXXX")
  chmod 0600 "$body"
  trap "rm -f -- $(printf '%q' "$body")" EXIT
  {
    printf '[ANTENNA_PUBLIC_GROUP v=1]\n'
    printf 'group_id: %s\n' "$group_id"
    printf '[/ANTENNA_PUBLIC_GROUP]\n\n'
    printf '%s' "$message"
  } >"$body"
  if [[ -n "$subject" ]]; then
    if send_output=$(bash "$SEND_SCRIPT" "$relay" --include-response --subject "$subject" --stdin <"$body"); then
      send_rc=0
    else
      send_rc=$?
    fi
  else
    if send_output=$(bash "$SEND_SCRIPT" "$relay" --include-response --stdin <"$body"); then
      send_rc=0
    else
      send_rc=$?
    fi
  fi
  printf '%s\n' "$send_output"
  (( send_rc == 0 )) || exit "$send_rc"
  failed=$(jq -er '.response.failed | select(type == "number" and . >= 0 and floor == .)' <<<"$send_output") \
    || die "ClawReef did not return Public Group delivery results" 5
  (( failed == 0 )) || die "Public Group fan-out reported $failed failed delivery attempt(s)" 5
}

# Share the route mutation lock with signed CLI reconciliation. Readers observe
# an atomic old/new file; do not hold this lock during network delivery.
case "${1:-}" in
  install|refresh|remove)
    [[ ! -L "$ROUTES_FILE.lock" ]] || die "Unsafe route lock"
    umask 077
    exec {route_lock_fd}>"$ROUTES_FILE.lock"
    [[ -f "$ROUTES_FILE.lock" && "$(stat -c '%u' "$ROUTES_FILE.lock")" -eq "$(id -u)" && "$(stat -c '%a' "$ROUTES_FILE.lock")" == "600" ]] || die "Unsafe route lock"
    flock -x "$route_lock_fd"
    ;;
esac

case "${1:-}" in
  list) list_groups ;;
  install) shift; install_routes "$@" ;;
  refresh) shift; refresh_routes "$@" ;;
  remove) shift; remove_route "$@" ;;
  send) shift; send_group "$@" ;;
  *)
    echo "Usage: antenna groups list" >&2
    echo "       antenna groups install <downloaded-route.json> [--alias <name>]" >&2
    echo "       antenna groups refresh <downloaded-route.json>" >&2
    echo "       antenna groups remove <alias>" >&2
    echo "       antenna groups send <alias> <message> [--subject <text>]" >&2
    echo "Public Groups are public: ClawReef reads and relays their plaintext." >&2
    exit 1
    ;;
esac
