#!/usr/bin/env bash
# lib/bundles.sh — Shared helpers for Antenna bootstrap bundles.
#
# SOURCE, don't execute. Callers must already have:
#   - SKILL_DIR set to the skill root
#   - $SKILL_DIR/lib/peers.sh sourced (provides validate_peer_url)
#
# Addresses REF-2000: promote bundle shape/freshness validation out of
# scripts/antenna-exchange.sh so it can be shared by `antenna-doctor.sh`,
# `antenna-bundle.sh`, and any future caller that needs to look at a
# bootstrap bundle without duplicating the jq expression.

# Guard against double-source.
if [[ -n "${_ANTENNA_LIB_BUNDLES_LOADED:-}" ]]; then
  return 0
fi
_ANTENNA_LIB_BUNDLES_LOADED=1

# Canonical jq shape predicate. Kept here so scripts/antenna-exchange.sh,
# scripts/antenna-bundle.sh, and scripts/antenna-doctor.sh all agree on
# what a valid bootstrap bundle looks like.
#
# Intentionally does NOT include URL shape — URL validation is handled
# separately by validate_peer_url so we can emit a specific reason when
# it's the URL that's wrong.
_ANTENNA_BUNDLE_SHAPE_PRED='
  .schema_version == 1 and
  .bundle_type == "antenna-bootstrap" and
  (.expires_at | type == "string" and test("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")) and
  (.from_peer_id | type == "string" and length > 0) and
  (.from_endpoint_url | type == "string" and length > 0) and
  (.from_hooks_token | type == "string" and length > 0) and
  (.from_identity_secret | type == "string" and test("^[0-9a-f]{64}$")) and
  (.from_exchange_pubkey | type == "string" and startswith("age1"))
'

# bundle_shape_reason <bundle_json_path>
#   Returns 0 if the JSON conforms to the canonical shape.
#   Returns 1 and echoes a single-line human reason to stderr on failure.
#
#   Checks fields one at a time so the reason is specific, not just
#   "bundle didn't match jq predicate".
bundle_shape_reason() {
  local bundle_json="$1"

  [[ -f "$bundle_json" ]] || { echo "bundle JSON file not found: $bundle_json" >&2; return 1; }

  # jq parse must succeed first; otherwise every later check is noise.
  if ! jq -e 'type == "object"' "$bundle_json" >/dev/null 2>&1; then
    echo "bundle is not a JSON object (parse failed)" >&2
    return 1
  fi

  local v

  v=$(jq -r '.schema_version // empty' "$bundle_json" 2>/dev/null)
  if [[ "$v" != "1" ]]; then
    echo "schema_version must be 1 (got: ${v:-<missing>})" >&2
    return 1
  fi

  v=$(jq -r '.bundle_type // empty' "$bundle_json" 2>/dev/null)
  if [[ "$v" != "antenna-bootstrap" ]]; then
    echo "bundle_type must be \"antenna-bootstrap\" (got: ${v:-<missing>})" >&2
    return 1
  fi

  v=$(jq -r '.expires_at // empty' "$bundle_json" 2>/dev/null)
  if [[ -z "$v" ]] || ! [[ "$v" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]]; then
    echo "expires_at missing or not an ISO-8601 Z timestamp (got: ${v:-<missing>})" >&2
    return 1
  fi

  v=$(jq -r '.from_peer_id // empty' "$bundle_json" 2>/dev/null)
  [[ -n "$v" ]] || { echo "from_peer_id missing or empty" >&2; return 1; }

  v=$(jq -r '.from_endpoint_url // empty' "$bundle_json" 2>/dev/null)
  [[ -n "$v" ]] || { echo "from_endpoint_url missing or empty" >&2; return 1; }

  v=$(jq -r '.from_hooks_token // empty' "$bundle_json" 2>/dev/null)
  [[ -n "$v" ]] || { echo "from_hooks_token missing or empty" >&2; return 1; }

  v=$(jq -r '.from_identity_secret // empty' "$bundle_json" 2>/dev/null)
  if ! [[ "$v" =~ ^[0-9a-f]{64}$ ]]; then
    echo "from_identity_secret must be 64 lowercase hex chars" >&2
    return 1
  fi

  v=$(jq -r '.from_exchange_pubkey // empty' "$bundle_json" 2>/dev/null)
  if [[ "$v" != age1* ]]; then
    echo "from_exchange_pubkey must start with \"age1\" (got: ${v:-<missing>})" >&2
    return 1
  fi

  return 0
}

# bundle_endpoint_url_reason <bundle_json_path>
#   Returns 0 if .from_endpoint_url passes validate_peer_url.
#   Returns 1 and echoes the reason.
#
#   Depends on validate_peer_url from lib/peers.sh.
bundle_endpoint_url_reason() {
  local bundle_json="$1"
  local endpoint reason
  endpoint=$(jq -r '.from_endpoint_url // empty' "$bundle_json" 2>/dev/null)
  if ! reason="$(validate_peer_url "$endpoint" false 2>&1 >/dev/null)"; then
    echo "from_endpoint_url invalid: ${reason:-invalid URL}" >&2
    return 1
  fi
  return 0
}

# bundle_freshness_state <bundle_json_path>
#   Echoes one of: fresh | expired | unknown
#   Exit code: 0 if fresh, 1 if expired or unknown (malformed timestamp).
#
#   "unknown" means the timestamp didn't parse or is missing; callers
#   should treat this as a hard failure but distinguishable from expired.
bundle_freshness_state() {
  local bundle_json="$1"
  local now expires_at
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  expires_at="$(jq -r '.expires_at // empty' "$bundle_json" 2>/dev/null)"

  if [[ -z "$expires_at" ]]; then
    echo "unknown"
    return 1
  fi

  if [[ "$expires_at" > "$now" || "$expires_at" == "$now" ]]; then
    echo "fresh"
    return 0
  fi

  echo "expired"
  return 1
}

# bundle_summary_json <bundle_json_path>
#   Emit a safe, operator-visible subset of the bundle as JSON. Drops
#   the sensitive fields (from_hooks_token, from_identity_secret) so the
#   summary can be printed and logged without leaking credentials.
bundle_summary_json() {
  local bundle_json="$1"
  jq '{
    schema_version,
    bundle_type,
    generated_at,
    expires_at,
    bundle_id,
    from_peer_id,
    from_display_name,
    from_endpoint_url,
    from_agent_id,
    from_exchange_pubkey,
    expected_peer_id,
    notes,
    has_hooks_token: ((.from_hooks_token // "") | length > 0),
    has_identity_secret: ((.from_identity_secret // "") | length > 0)
  }' "$bundle_json" 2>/dev/null
}
