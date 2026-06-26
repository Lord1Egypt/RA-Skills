#!/usr/bin/env bash
# lib/config.sh — read-only helpers for antenna-config.json.
#
# Contract:
#   - Every helper prints a string to stdout (no trailing newline beyond one).
#   - Missing $CONFIG_FILE → helper returns its default, silently, exit 0.
#   - Missing key → helper returns its default, silently, exit 0.
#   - Corrupt JSON → helper returns its default AND prints one warning
#     line to stderr ("antenna: config read failed, using defaults").
#     First-warning-wins per-process to avoid log spam.
#   - Booleans are always "true" or "false" strings.
#   - Empty-default keys return the empty string (not "null").
#
# Sourcing:
#   Requires $CONFIG_FILE to be set by the caller before any helper
#   is invoked. Typical source block:
#
#       CONFIG_FILE="$SKILL_DIR/antenna-config.json"
#       . "$SKILL_DIR/lib/config.sh"

_antenna_config_warned=0

_config_read() {
  local jq_path="$1" default="${2-}"

  if [[ -z "${CONFIG_FILE:-}" || ! -f "$CONFIG_FILE" ]]; then
    printf '%s' "$default"
    return 0
  fi

  local v rc
  v=$(jq -r "${jq_path} // empty" "$CONFIG_FILE" 2>/dev/null)
  rc=$?

  if (( rc != 0 )); then
    if (( _antenna_config_warned == 0 )); then
      printf 'antenna: config read failed, using defaults\n' >&2
      _antenna_config_warned=1
    fi
    printf '%s' "$default"
    return 0
  fi

  if [[ -z "$v" ]]; then
    printf '%s' "$default"
  else
    printf '%s' "$v"
  fi
}

# ── Hot keys: one helper per canonical config field ──
config_log_path()               { _config_read '.log_path' 'antenna.log'; }
config_log_enabled()            { _config_read '.log_enabled' 'true'; }
config_log_verbose()            { _config_read '.log_verbose' 'false'; }
config_local_agent_id()         { _config_read '.local_agent_id' 'agent'; }
config_max_message_length()     { _config_read '.max_message_length' '10000'; }
config_relay_agent_model()      { _config_read '.relay_agent_model' 'unset'; }
config_relay_agent_id()         { _config_read '.relay_agent_id' 'antenna'; }
config_default_target_session() { _config_read '.default_target_session' ''; }
config_inbox_enabled()          { _config_read '.inbox_enabled' 'false'; }
config_inbox_queue_path()       { _config_read '.inbox_queue_path' 'antenna-inbox.json'; }
config_mcs_enabled()            { _config_read '.mcs_enabled' 'false'; }
config_rate_limit_per_peer()    { _config_read '.rate_limit.per_peer_per_minute' '10'; }
config_rate_limit_global()      { _config_read '.rate_limit.global_per_minute' '30'; }

# ── Generic escape hatch for ad-hoc reads ──
# Usage: v=$(config_get '.some.jq.path' [default])
config_get() {
  local jq_path="$1" default="${2-}"
  _config_read "$jq_path" "$default"
}

# ── Writers ─────────────────────────────────────────────────────────────────
#
# All writers share the same atomic-write discipline:
#   1. $CONFIG_FILE must exist (writers never create it — that's setup's job).
#   2. Run jq into a mktemp file in the same directory (so mv is atomic on
#      the same filesystem).
#   3. If jq fails, the temp file is removed and the original is untouched.
#   4. On success, mv replaces $CONFIG_FILE atomically.
#   5. File permissions of $CONFIG_FILE are preserved across the swap.
#
# Writers never touch gateway.json — relay_agent_model sync is still done
# at the callsite in bin/antenna.sh (_sync_relay_model_to_gateway).

# config_mutate <jq_filter> [jq_args...]
#   Runs `jq <args> '<filter>' $CONFIG_FILE` and atomically swaps the result
#   in place. Returns non-zero (and preserves the original file) if jq fails
#   or $CONFIG_FILE is missing.
config_mutate() {
  if [[ -z "${CONFIG_FILE:-}" || ! -f "$CONFIG_FILE" ]]; then
    printf 'antenna: config_mutate: CONFIG_FILE unset or missing\n' >&2
    return 1
  fi

  local filter="$1"; shift
  local dir; dir=$(dirname -- "$CONFIG_FILE")
  local tmp; tmp=$(mktemp "$dir/.antenna-config.XXXXXX") || return 1

  if ! jq "$@" "$filter" "$CONFIG_FILE" > "$tmp" 2>/dev/null; then
    rm -f "$tmp"
    printf 'antenna: config_mutate: jq filter failed\n' >&2
    return 1
  fi

  # Preserve perms across the swap.
  local perms
  perms=$(stat -c '%a' "$CONFIG_FILE" 2>/dev/null \
          || stat -f '%Lp' "$CONFIG_FILE" 2>/dev/null \
          || echo '')
  if [[ -n "$perms" ]]; then
    chmod "$perms" "$tmp" 2>/dev/null || true
  fi

  mv -- "$tmp" "$CONFIG_FILE"
}

# config_set_field <key> <value>
#   Set a top-level field. Tries to interpret <value> as JSON (number,
#   bool, array, object); falls back to string. Mirrors the behavior of
#   `antenna config set` so both paths agree.
config_set_field() {
  local key="$1" value="$2"

  if echo "$value" | jq -e '.' >/dev/null 2>&1; then
    config_mutate '.[$k] = $v' --arg k "$key" --argjson v "$value" && return 0
    # Fallback if argjson rejected e.g. a bare word that happened to parse.
    config_mutate '.[$k] = $v' --arg k "$key" --arg v "$value"
  else
    config_mutate '.[$k] = $v' --arg k "$key" --arg v "$value"
  fi
}

# config_set_relay_model <model>
#   Convenience writer for `.relay_agent_model`. Gateway sync is the
#   caller's responsibility (see bin/antenna.sh _sync_relay_model_to_gateway).
config_set_relay_model() {
  config_mutate '.relay_agent_model = $m' --arg m "$1"
}
