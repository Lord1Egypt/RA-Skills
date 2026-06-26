# lib/peers.sh — Shared helpers for reading antenna-peers.json
#
# SOURCE, don't execute. Callers must set PEERS_FILE before sourcing or before
# calling any helper. All helpers are read-only; mutations stay with their
# owning scripts (antenna-exchange.sh, antenna-peers.sh).
#
# Conventions:
#   - Helpers emit their result to stdout; empty string means "not found".
#   - `peers_exists` returns 0/1 via exit code.
#   - `peers_require` emits on stdout OR dies with a helpful message.
#   - Missing/invalid peers file is tolerated silently (stdout empty),
#     matching the legacy inline behavior. Callers that need strictness
#     should use `peers_require` or check `peers_exists` first.
#
# Addresses: REF-1303, REF-1405, REF-1513 (duplicated jq patterns).

# Guard against double-source.
if [[ -n "${_ANTENNA_LIB_PEERS_LOADED:-}" ]]; then
  return 0
fi
_ANTENNA_LIB_PEERS_LOADED=1

# Canonical jq predicate: "object with a url string field".
# Keeps the shape in ONE place; everything else composes on it.
_ANTENNA_PEER_OBJ_PRED='(.value | type) == "object" and (.value.url? | type) == "string"'

# peers_list_ids
#   Emits every peer ID that has a url field, one per line.
peers_list_ids() {
  [[ -f "${PEERS_FILE:-}" ]] || return 0
  jq -r "to_entries[] | select($_ANTENNA_PEER_OBJ_PRED) | .key" \
    "$PEERS_FILE" 2>/dev/null || true
}

# peers_list_self_ids
#   Emits every peer ID marked self==true (should be 0 or 1).
peers_list_self_ids() {
  [[ -f "${PEERS_FILE:-}" ]] || return 0
  jq -r "to_entries[] | select($_ANTENNA_PEER_OBJ_PRED and .value.self == true) | .key" \
    "$PEERS_FILE" 2>/dev/null || true
}

# peers_self_id
#   First self peer's ID, or empty.
peers_self_id() {
  peers_list_self_ids | head -n 1
}

# peers_self_url
#   First self peer's url, or empty.
peers_self_url() {
  [[ -f "${PEERS_FILE:-}" ]] || return 0
  jq -r "to_entries[] | select($_ANTENNA_PEER_OBJ_PRED and .value.self == true) | .value.url" \
    "$PEERS_FILE" 2>/dev/null | head -n 1
}

# peers_exists <peer_id>
#   Exit 0 if peer key exists in the file, 1 otherwise.
peers_exists() {
  local peer="${1:-}"
  [[ -n "$peer" ]] || return 1
  [[ -f "${PEERS_FILE:-}" ]] || return 1
  jq -e --arg p "$peer" 'has($p)' "$PEERS_FILE" >/dev/null 2>&1
}

# peers_get <peer_id> <field>
#   Emits .[peer][field] or empty if missing.
peers_get() {
  local peer="${1:-}" field="${2:-}"
  [[ -n "$peer" && -n "$field" ]] || return 0
  [[ -f "${PEERS_FILE:-}" ]] || return 0
  jq -r --arg p "$peer" --arg f "$field" '.[$p][$f] // empty' \
    "$PEERS_FILE" 2>/dev/null || true
}

# peers_require <peer_id> <field> <context>
#   Emits .[peer][field] or writes an error to stderr and exits 1.
#   <context> is a short phrase used in the error (e.g. "antenna send").
peers_require() {
  local peer="${1:-}" field="${2:-}" ctx="${3:-antenna}"
  local val
  val="$(peers_get "$peer" "$field")"
  if [[ -z "$val" ]]; then
    echo "$ctx: peer '$peer' is missing required field '$field' in ${PEERS_FILE:-antenna-peers.json}" >&2
    exit 1
  fi
  printf '%s\n' "$val"
}

# validate_peer_url <url> [allow_insecure]
#   Returns 0 if <url> looks like a plausible hook endpoint, 1 otherwise.
#   Prints a one-line reason to stderr on failure (no color, no prefix).
#
#   Policy (REF-1313):
#     - Must start with https:// (or http:// when allow_insecure == "true").
#     - Must have a non-empty host component (reject bare scheme).
#     - Must not contain whitespace or control characters.
#     - Host must contain at least one dot OR be "localhost" (with optional port).
#       This rejects garbage-but-plausible strings like "main", "foo", "bar" that
#       technically survive a URL-parse but cannot possibly be a reachable peer.
#     - Trailing slash is tolerated; callers already strip it upstream.
#     - Query strings and fragments are rejected — a hook URL is a base endpoint,
#       not a pre-parameterized GET. This keeps the surface tight for v1.
#
#   Design notes:
#     - Pure bash regex, no curl/jq/python dependencies. Runs in setup's early
#       bootstrap path too.
#     - Single source of truth: every write boundary (setup, bundle build,
#       bundle import, peer add/update) calls this. REF-1313.
#     - Callers decide whether to `die` or `warn`; this helper does not exit.
validate_peer_url() {
  local url="${1:-}" allow_insecure="${2:-false}"

  if [[ -z "$url" ]]; then
    echo "peer URL is empty" >&2
    return 1
  fi

  # Reject whitespace / control chars outright.
  if [[ "$url" =~ [[:space:][:cntrl:]] ]]; then
    echo "peer URL contains whitespace or control characters: '$url'" >&2
    return 1
  fi

  # Scheme check.
  local scheme_ok=false
  if [[ "$url" =~ ^https:// ]]; then
    scheme_ok=true
  elif [[ "$url" =~ ^http:// && "$allow_insecure" == "true" ]]; then
    scheme_ok=true
  fi
  if [[ "$scheme_ok" != "true" ]]; then
    if [[ "$allow_insecure" == "true" ]]; then
      echo "peer URL must start with https:// or http:// (got: '$url')" >&2
    else
      echo "peer URL must start with https:// (got: '$url'; pass --allow-insecure to permit http://)" >&2
    fi
    return 1
  fi

  # Strip scheme, then isolate host[:port] (everything up to first '/' or '?').
  local rest="${url#*://}"
  # Reject query/fragment in base endpoint.
  if [[ "$rest" == *\?* || "$rest" == *\#* ]]; then
    echo "peer URL must not contain query string or fragment: '$url'" >&2
    return 1
  fi
  local hostport="${rest%%/*}"
  if [[ -z "$hostport" ]]; then
    echo "peer URL is missing a host: '$url'" >&2
    return 1
  fi
  # Strip port (if any) for the dotted-host sanity check; keep the full
  # hostport for the localhost match so "localhost:8080" still counts.
  local host="${hostport%%:*}"
  if [[ -z "$host" ]]; then
    echo "peer URL host is empty: '$url'" >&2
    return 1
  fi

  # Host must contain a dot (FQDN / IPv4) OR be exactly "localhost".
  # This is the check that finally catches things like url="main".
  if [[ "$host" != "localhost" && "$host" != *.* ]]; then
    echo "peer URL host '$host' does not look like a reachable hostname (no dot, not 'localhost'): '$url'" >&2
    return 1
  fi

  return 0
}
