#!/usr/bin/env bash
# scripts/antenna-bundle.sh — operator-facing bundle inspection.
#
# REF-2000: expose `antenna bundle verify <file>` so operators can sanity-
# check a received `.age.txt` bootstrap bundle before deciding to import it.
# Uses lib/bundles.sh shape validator so the exchange importer and this
# verifier agree on what "valid" means.
#
# Subcommands:
#   verify <file>   Decrypt with the local exchange key, check shape,
#                   check freshness, print a summary. Does NOT import.
#                   Supports: --json, --force-expired, --no-decrypt
#
# Exit codes:
#   0   bundle passed all checks
#   1   file missing, shape failure, URL shape failure, or expired
#       (without --force-expired)
#   2   decryption failed (wrong key, not an age file, etc.)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SECRETS_DIR="$SKILL_DIR/secrets"
EXCHANGE_KEY_FILE="$SECRETS_DIR/antenna-exchange.agekey"

PEERS_FILE="$SKILL_DIR/antenna-peers.json"
CONFIG_FILE="$SKILL_DIR/antenna-config.json"

# Sourced libs provide validate_peer_url and the bundle helpers.
# shellcheck disable=SC1091
source "$SKILL_DIR/lib/peers.sh"
# shellcheck disable=SC1091
source "$SKILL_DIR/lib/bundles.sh"

# ── Output helpers ────────────────────────────────────────────────────────
_has_tty() { [[ -t 1 ]]; }
if _has_tty && [[ -z "${NO_COLOR:-}" ]]; then
  C_RESET=$'\033[0m'; C_GREEN=$'\033[0;32m'; C_RED=$'\033[0;31m'
  C_YEL=$'\033[1;33m'; C_CYAN=$'\033[0;36m'
else
  C_RESET=""; C_GREEN=""; C_RED=""; C_YEL=""; C_CYAN=""
fi

pass() { printf '  %s✓%s %s\n' "$C_GREEN" "$C_RESET" "$1"; }
warn() { printf '  %s⚠%s %s\n' "$C_YEL"   "$C_RESET" "$1"; }
fail() { printf '  %s✗%s %s\n' "$C_RED"   "$C_RESET" "$1"; }
info() { printf '  %sℹ%s %s\n' "$C_CYAN"  "$C_RESET" "$1"; }

usage() {
  cat <<'EOF'
Usage:
  antenna bundle verify <file> [options]

Options:
  --json              Emit a machine-readable JSON verdict instead of
                      human output. Exit code still reflects validity.
  --force-expired     Do not fail if the bundle's expires_at is in the past.
  --no-decrypt        Treat <file> as already-decrypted bundle JSON (do
                      not run age). Useful for piping already-decrypted
                      content through the validator.

Notes:
  - Decryption uses the local exchange key at
    skills/antenna/secrets/antenna-exchange.agekey.
  - This command NEVER writes to antenna-peers.json. It only reads.
  - Sensitive fields (from_hooks_token, from_identity_secret) are never
    printed; the summary shows only their presence.
EOF
}

cmd_verify() {
  local file=""
  local json_mode=false
  local force_expired=false
  local no_decrypt=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --json) json_mode=true; shift ;;
      --force-expired) force_expired=true; shift ;;
      --no-decrypt) no_decrypt=true; shift ;;
      -h|--help) usage; exit 0 ;;
      -*)
        echo "Unknown option: $1" >&2
        usage >&2
        exit 2
        ;;
      *)
        if [[ -z "$file" ]]; then
          file="$1"
        else
          echo "Unexpected extra argument: $1" >&2
          exit 2
        fi
        shift
        ;;
    esac
  done

  if [[ -z "$file" ]]; then
    echo "antenna bundle verify: missing <file>" >&2
    usage >&2
    exit 2
  fi

  if [[ ! -f "$file" ]]; then
    if $json_mode; then
      jq -n --arg f "$file" '{ok:false, file:$f, reason:"file not found"}'
    else
      fail "File not found: $file"
    fi
    exit 1
  fi

  # Track failures as reasons so JSON mode reports all, not just the first.
  local reasons=()
  local warnings=()
  local json_out=""

  # ── Step 1: obtain bundle JSON ────────────────────────────────────────
  local bundle_json
  if $no_decrypt; then
    bundle_json="$file"
    $json_mode || info "Skipping decryption (--no-decrypt); reading as JSON."
  else
    if ! command -v age >/dev/null 2>&1; then
      if $json_mode; then
        jq -n --arg f "$file" '{ok:false, file:$f, reason:"age binary not found"}'
      else
        fail "age binary not found in PATH. Install age or use --no-decrypt."
      fi
      exit 2
    fi
    if [[ ! -f "$EXCHANGE_KEY_FILE" ]]; then
      if $json_mode; then
        jq -n --arg f "$file" --arg k "$EXCHANGE_KEY_FILE" \
          '{ok:false, file:$f, reason:"exchange key missing", key_path:$k}'
      else
        fail "Exchange key missing: $EXCHANGE_KEY_FILE"
        info "Run 'antenna peers exchange keygen' to create one."
      fi
      exit 2
    fi

    bundle_json=$(mktemp)
    trap 'rm -f "$bundle_json"' EXIT

    if ! age -d -i "$EXCHANGE_KEY_FILE" -o "$bundle_json" "$file" 2>/dev/null; then
      if $json_mode; then
        jq -n --arg f "$file" '{ok:false, file:$f, reason:"decrypt failed"}'
      else
        fail "Decryption failed."
        info "Either the file is not an age-encrypted Antenna bundle, or"
        info "it was encrypted for a different recipient. The bundle ID"
        info "shown by the sender must match the key you hold here."
      fi
      exit 2
    fi
    $json_mode || pass "Decrypted with local exchange key"
  fi

  # ── Step 2: shape validation ──────────────────────────────────────────
  local shape_reason=""
  if shape_reason=$(bundle_shape_reason "$bundle_json" 2>&1 >/dev/null); then
    shape_reason=""
    $json_mode || pass "Shape OK (schema_version, bundle_type, required fields present)"
  else
    reasons+=("shape: $shape_reason")
    $json_mode || fail "Shape invalid: $shape_reason"
  fi

  # ── Step 3: URL shape ─────────────────────────────────────────────────
  # Only meaningful if shape itself passed far enough for from_endpoint_url
  # to exist. If shape already failed on that field, skip to avoid a
  # duplicate reason.
  if [[ -z "$shape_reason" || "$shape_reason" != *"from_endpoint_url"* ]]; then
    local url_reason=""
    if url_reason=$(bundle_endpoint_url_reason "$bundle_json" 2>&1 >/dev/null); then
      url_reason=""
      $json_mode || pass "from_endpoint_url passes URL shape validation"
    else
      reasons+=("endpoint_url: $url_reason")
      $json_mode || fail "Endpoint URL invalid: $url_reason"
    fi
  fi

  # ── Step 4: freshness ─────────────────────────────────────────────────
  local freshness
  freshness=$(bundle_freshness_state "$bundle_json" 2>/dev/null || true)
  case "$freshness" in
    fresh)
      $json_mode || pass "Bundle is fresh (expires_at in the future)"
      ;;
    expired)
      if $force_expired; then
        warnings+=("expired (ignored via --force-expired)")
        $json_mode || warn "Bundle is expired; ignoring because --force-expired was set"
      else
        reasons+=("expired: expires_at is in the past")
        $json_mode || fail "Bundle is expired. Re-run with --force-expired to inspect anyway."
      fi
      ;;
    unknown|*)
      reasons+=("freshness: expires_at missing or malformed")
      $json_mode || fail "expires_at missing or malformed"
      ;;
  esac

  # ── Step 5: sensitive-field presence (signal, not value) ──────────────
  local has_tok has_sec
  has_tok=$(jq -r '(.from_hooks_token // "") | length' "$bundle_json" 2>/dev/null)
  has_sec=$(jq -r '(.from_identity_secret // "") | length' "$bundle_json" 2>/dev/null)
  if [[ "$has_tok" == "0" || -z "$has_tok" ]]; then
    reasons+=("sensitive: from_hooks_token missing")
    $json_mode || fail "from_hooks_token is missing (would break relay auth on import)"
  fi
  if [[ "$has_sec" == "0" || -z "$has_sec" ]]; then
    reasons+=("sensitive: from_identity_secret missing")
    $json_mode || fail "from_identity_secret is missing"
  fi

  # ── Summary ───────────────────────────────────────────────────────────
  local ok="true"
  [[ ${#reasons[@]} -eq 0 ]] || ok="false"

  if $json_mode; then
    # Build JSON verdict. Summary is safe (sensitive fields stripped).
    local summary
    summary=$(bundle_summary_json "$bundle_json" 2>/dev/null || echo '{}')
    jq -n \
      --arg file "$file" \
      --argjson ok "$ok" \
      --arg freshness "${freshness:-unknown}" \
      --argjson reasons "$(printf '%s\n' "${reasons[@]+"${reasons[@]}"}" | jq -R . | jq -s .)" \
      --argjson warnings "$(printf '%s\n' "${warnings[@]+"${warnings[@]}"}" | jq -R . | jq -s .)" \
      --argjson summary "$summary" \
      '{
        ok: $ok,
        file: $file,
        freshness: $freshness,
        reasons: ($reasons | map(select(length > 0))),
        warnings: ($warnings | map(select(length > 0))),
        summary: $summary
      }'
  else
    echo
    echo "── Bundle summary ──"
    local peer_id display_name endpoint agent_id generated_at expires_at bundle_id pubkey expected notes
    peer_id=$(jq -r '.from_peer_id // "—"' "$bundle_json" 2>/dev/null)
    display_name=$(jq -r '.from_display_name // "—"' "$bundle_json" 2>/dev/null)
    endpoint=$(jq -r '.from_endpoint_url // "—"' "$bundle_json" 2>/dev/null)
    agent_id=$(jq -r '.from_agent_id // "antenna"' "$bundle_json" 2>/dev/null)
    generated_at=$(jq -r '.generated_at // "—"' "$bundle_json" 2>/dev/null)
    expires_at=$(jq -r '.expires_at // "—"' "$bundle_json" 2>/dev/null)
    bundle_id=$(jq -r '.bundle_id // "—"' "$bundle_json" 2>/dev/null)
    pubkey=$(jq -r '.from_exchange_pubkey // "—"' "$bundle_json" 2>/dev/null)
    expected=$(jq -r '.expected_peer_id // "—"' "$bundle_json" 2>/dev/null)
    notes=$(jq -r '.notes // "—"' "$bundle_json" 2>/dev/null)
    printf '  Peer ID:        %s\n' "$peer_id"
    printf '  Display name:   %s\n' "$display_name"
    printf '  Endpoint URL:   %s\n' "$endpoint"
    printf '  Agent ID:       %s\n' "$agent_id"
    printf '  Generated at:   %s\n' "$generated_at"
    printf '  Expires at:     %s\n' "$expires_at"
    printf '  Bundle ID:      %s\n' "$bundle_id"
    printf '  Exchange pubkey:%s\n' "$pubkey"
    printf '  Expected peer:  %s\n' "$expected"
    printf '  Notes:          %s\n' "$notes"
    echo

    if [[ "$ok" == "true" ]]; then
      pass "Bundle verification passed"
    else
      fail "Bundle verification FAILED (${#reasons[@]} issue(s))"
    fi
  fi

  [[ "$ok" == "true" ]] && exit 0 || exit 1
}

subcmd="${1:-}"
shift || true

case "$subcmd" in
  verify) cmd_verify "$@" ;;
  help|-h|--help|"") usage ;;
  *)
    echo "Unknown subcommand: $subcmd" >&2
    usage >&2
    exit 2
    ;;
esac
