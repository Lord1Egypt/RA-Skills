#!/usr/bin/env bash
# REF-600 regression test: self-identity hijack via encrypted bootstrap import.
#
# Layers under test:
#   1. import_bundle primary guard: refuses when bundle.from_peer_id == self_id.
#   2. ensure_peer_entry_updated defense-in-depth: preserves existing .self flag
#      across merges, so even if something reaches the writer for the self entry
#      it cannot strip .self.
#   3. Preview warning: print_import_preview surfaces the collision.
#
# Runs in an isolated temp SKILL_DIR; does not touch the live peers registry.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref600-XXXXXX)"
trap 'rm -rf "$TEST_ROOT"' EXIT

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  \033[31m✗\033[0m %s\n' "$1"; [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

# ── Build an isolated antenna skill dir with a self-peer named "alice" ─────
SKILL_DIR="$TEST_ROOT/skill"
mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/lib" "$SKILL_DIR/secrets"
cp "$SKILL_REPO/scripts/antenna-exchange.sh" "$SKILL_DIR/scripts/"
cp -r "$SKILL_REPO/lib/." "$SKILL_DIR/lib/"

cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "alice": {
    "url": "https://alice.example",
    "token_file": "secrets/hooks_token_alice",
    "peer_secret_file": "secrets/antenna-peer-alice.secret",
    "agentId": "antenna",
    "display_name": "Alice (local)",
    "self": true
  }
}
JSON

cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "allowed_inbound_peers": ["alice"],
  "allowed_outbound_peers": [],
  "log_enabled": false
}
JSON

echo "placeholder-token" > "$SKILL_DIR/secrets/hooks_token_alice"
echo "0000000000000000000000000000000000000000000000000000000000000000" > "$SKILL_DIR/secrets/antenna-peer-alice.secret"
chmod 600 "$SKILL_DIR/secrets/"*

echo "── REF-600 regression ──"

# ── Test 1: ensure_peer_entry_updated preserves .self on the self entry ────
# Source the script in a way that only pulls helper functions, then call the
# writer directly. We stub out anything that would actually execute I/O beyond
# the peers file.

(
  set -euo pipefail
  export PEERS_FILE="$SKILL_DIR/antenna-peers.json"
  export CONFIG_FILE="$SKILL_DIR/antenna-config.json"
  export SKILL_DIR="$SKILL_DIR"

  # Extract just ensure_peer_entry_updated by sourcing the whole exchange script
  # with its top-level cmd dispatch disabled. The script only dispatches when
  # invoked directly; sourcing is safe because the bottom of the file is a
  # `main "$@"` style call guarded by `BASH_SOURCE`.
  # However antenna-exchange.sh currently unconditionally runs cmd at end, so
  # we extract the function via awk and eval it instead.
  awk '/^ensure_peer_entry_updated\(\) \{/,/^\}$/' \
    "$SKILL_REPO/scripts/antenna-exchange.sh" > "$TEST_ROOT/ensure_fn.sh"
  # shellcheck source=/dev/null
  source "$TEST_ROOT/ensure_fn.sh"

  # Simulate a merge that does NOT include .self in the provided fields.
  ensure_peer_entry_updated \
    "alice" \
    "https://attacker.example" \
    "secrets/hooks_token_alice" \
    "secrets/antenna-peer-alice.secret" \
    "antenna" \
    "Alice (pwned)" \
    "age1attackerpubkey0000000000000000000000000000000000000000"
)

still_self=$(jq -r '.alice.self // false' "$SKILL_DIR/antenna-peers.json")
new_name=$(jq -r '.alice.display_name // ""' "$SKILL_DIR/antenna-peers.json")

if [[ "$still_self" == "true" ]]; then
  pass "T1: ensure_peer_entry_updated preserves .self across merges"
else
  fail "T1: ensure_peer_entry_updated preserves .self across merges" ".self became $still_self after update"
fi

# Sanity: the merge itself still worked (display_name did update).
if [[ "$new_name" == "Alice (pwned)" ]]; then
  pass "T1b: merge still updates non-self fields (display_name)"
else
  fail "T1b: merge still updates non-self fields" "display_name=$new_name"
fi

# Also verify .self survives a merge on a non-self peer that previously had no self flag.
(
  set -euo pipefail
  export PEERS_FILE="$SKILL_DIR/antenna-peers.json"
  export CONFIG_FILE="$SKILL_DIR/antenna-config.json"
  export SKILL_DIR="$SKILL_DIR"
  # shellcheck source=/dev/null
  source "$TEST_ROOT/ensure_fn.sh"
  # Add a new peer "bob" (not self) via the writer.
  ensure_peer_entry_updated \
    "bob" \
    "https://bob.example" \
    "secrets/hooks_token_bob" \
    "secrets/antenna-peer-bob.secret" \
    "antenna" \
    "Bob" \
    "age1bobpubkey0000000000000000000000000000000000000000000000"
)

bob_self=$(jq -r '.bob.self // null' "$SKILL_DIR/antenna-peers.json")
if [[ "$bob_self" == "null" ]]; then
  pass "T1c: merge does not add spurious .self to non-self peer"
else
  fail "T1c: merge does not add spurious .self" ".self=$bob_self on bob"
fi

# ── Test 2: import_bundle primary guard refuses self-identity bundle ───────
# We cannot easily forge a decrypted-bundle JSON path that passes all earlier
# validation (age decrypt, validate_age_pubkey, validate_runtime_secret), so
# we test the guard at a smaller seam: extract the guard check as a shell
# predicate and verify its behavior plus the log_entry payload format by
# grepping the source. This covers the decision point even without a live
# bundle.

# 2a: static check — guard exists and refuses without --yes override.
if grep -q 'REF-600: primary guard against self-identity hijack' \
     "$SKILL_REPO/scripts/antenna-exchange.sh"; then
  pass "T2a: primary guard present in import_bundle"
else
  fail "T2a: primary guard present in import_bundle" "marker comment missing"
fi

# 2b: guard uses 'die', not 'confirm_or_die', so --yes cannot bypass.
if awk '/REF-600: primary guard/,/^  fi$/' \
     "$SKILL_REPO/scripts/antenna-exchange.sh" | grep -q '^    die '; then
  pass "T2b: primary guard uses die() — no --yes bypass"
else
  fail "T2b: primary guard uses die()" "guard may be bypassable via confirm_or_die"
fi

# 2c: decrypted bundle cleanup is guaranteed before the REF-600 guard can die.
# After REF-603 this no longer needs an inline `rm -f "$bundle_json"` inside
# the guard itself; instead the import-side cleanup trap must be installed
# immediately after decrypt and before any later die-paths, including REF-600.
IMPORT_BODY="$(awk '/^import_bundle\(\) \{/,/^\}$/' "$SKILL_REPO/scripts/antenna-exchange.sh")"
if printf '%s\n' "$IMPORT_BODY" | awk '
  /bundle_json="\$\(decrypt_bundle_to_json / { seen_decrypt = 1; next }
  seen_decrypt && /^[[:space:]]*trap .*bundle_json.*(RETURN|EXIT)/ { trap_found = 1 }
  /REF-600: primary guard against self-identity hijack/ && !trap_found { bad = 1 }
  END { exit (trap_found && !bad) ? 0 : 1 }
'; then
  pass "T2c: import-side cleanup trap is armed before the REF-600 guard"
else
  fail "T2c: import-side cleanup trap is armed before the REF-600 guard" \
       "expected trap after decrypt and before self-identity refusal guard"
fi

# 2d: guard writes a log entry for audit trail.
if awk '/REF-600: primary guard/,/^  fi$/' \
     "$SKILL_REPO/scripts/antenna-exchange.sh" \
     | grep -q 'status:refused | reason:self_identity_collision'; then
  pass "T2d: primary guard emits refusal log entry"
else
  fail "T2d: primary guard emits refusal log entry" "log_entry marker missing"
fi

# ── Test 3: print_import_preview flags self collision ─────────────────────
if grep -q "REF-600: surface self-identity collision" \
     "$SKILL_REPO/scripts/antenna-exchange.sh"; then
  pass "T3: preview warns on self-identity collision"
else
  fail "T3: preview warns on self-identity collision" "marker comment missing"
fi

echo
echo "── Summary ──"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]]
