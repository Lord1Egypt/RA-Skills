#!/usr/bin/env bash
# REF-300 / REF-303 regression test: peers add overwrite + merge semantics.
#
# Semantics under test:
#   1. Adding a brand-new peer still works and requires --url / --token-file.
#   2. Re-adding an existing peer without --force is refused and leaves the
#      registry untouched (REF-300: no silent overwrite).
#   3. --force with only --display-name merges: url, token_file, and any
#      unknown top-level fields (e.g. .self) are preserved (REF-303: no
#      unconditional null-out).
#   4. --force with only --exchange-public-key merges the same way.
#   5. --force on a new-id is allowed but still requires --url / --token-file
#      because the peer does not yet exist.
#   6. Unknown options are still rejected.
#
# Runs against an isolated $SKILL_DIR; does not touch the live registry.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref300-XXXXXX)"
trap 'rm -rf "$TEST_ROOT"' EXIT

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  \033[31m✗\033[0m %s\n' "$1"; [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

# ── Build an isolated SKILL_DIR copy with just enough to run `antenna peers add` ─
SKILL_DIR="$TEST_ROOT/skill"
mkdir -p "$SKILL_DIR/bin" "$SKILL_DIR/lib" "$SKILL_DIR/secrets"
cp "$SKILL_REPO/bin/antenna.sh" "$SKILL_DIR/bin/"
cp -r "$SKILL_REPO/lib/." "$SKILL_DIR/lib/"

# Minimal antenna-config.json so the CLI's config loader doesn't explode.
cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "self_id": "testhost",
  "display_name": "Test Host",
  "relay_agent_model": "unset",
  "allowed_inbound_peers": [],
  "allowed_outbound_peers": [],
  "allowed_inbound_sessions": []
}
JSON

# Seed a peers registry with an existing peer that carries an unknown field
# (.self) and an exchange_public_key. This simulates the post-exchange state.
cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "alice": {
    "url": "https://alice.example",
    "token_file": "secrets/hooks_token_alice",
    "agentId": "antenna",
    "display_name": "Alice (original)",
    "peer_secret_file": "secrets/antenna-peer-alice.secret",
    "exchange_public_key": "age1original",
    "self": false
  }
}
JSON

cp "$SKILL_REPO/antenna-config.schema.json" "$SKILL_DIR/" 2>/dev/null || true

# Drive bin/antenna.sh with SKILL_DIR pinned to our tempdir so it reads/writes
# our scratch registry instead of the real one.
run_peers_add() {
  (
    cd "$SKILL_DIR"
    SKILL_DIR="$SKILL_DIR" bash "$SKILL_DIR/bin/antenna.sh" peers add "$@"
  )
}

PEERS_FILE="$SKILL_DIR/antenna-peers.json"
snapshot() { cat "$PEERS_FILE"; }
field() { jq -r --arg id "$1" --arg k "$2" '.[$id][$k]' "$PEERS_FILE"; }

echo "── REF-300 / REF-303: peers add overwrite + merge semantics ─────────────"
echo ""

# ── Test 1: fresh add works and writes expected fields ────────────────────
run_peers_add bob --url https://bob.example --token-file secrets/hooks_token_bob >/dev/null 2>&1 \
  && pass "fresh add: bob created without --force" \
  || fail "fresh add: bob should have been created"

[[ "$(field bob url)" == "https://bob.example" ]] \
  && pass "fresh add: bob.url written" \
  || fail "fresh add: bob.url missing"

[[ "$(field bob token_file)" == "secrets/hooks_token_bob" ]] \
  && pass "fresh add: bob.token_file written" \
  || fail "fresh add: bob.token_file missing"

[[ "$(field bob agentId)" == "antenna" ]] \
  && pass "fresh add: bob.agentId defaulted to 'antenna'" \
  || fail "fresh add: bob.agentId wrong"

# ── Test 2: fresh add without --url / --token-file is refused ─────────────
if run_peers_add carol >/dev/null 2>&1; then
  fail "fresh add: missing --url/--token-file should be refused"
else
  pass "fresh add: missing --url/--token-file refused"
fi

# ── Test 3: re-add without --force is refused, registry untouched ─────────
BEFORE="$(snapshot)"
if run_peers_add alice --url https://evil.example --token-file secrets/evil >/dev/null 2>&1; then
  fail "re-add alice without --force should be refused"
else
  pass "re-add without --force: refused with non-zero exit"
fi
AFTER="$(snapshot)"
if [[ "$BEFORE" == "$AFTER" ]]; then
  pass "re-add without --force: registry unchanged"
else
  fail "re-add without --force: registry was modified"
fi

# ── Test 4: --force --display-name only merges, preserves everything else ─
run_peers_add alice --force --display-name "Alice (renamed)" >/dev/null 2>&1 \
  && pass "force update alice --display-name: succeeded" \
  || fail "force update alice --display-name: should have succeeded"

[[ "$(field alice display_name)" == "Alice (renamed)" ]] \
  && pass "merge: display_name updated" \
  || fail "merge: display_name not updated"

[[ "$(field alice url)" == "https://alice.example" ]] \
  && pass "merge: url preserved (not null-ed out)" \
  || fail "merge: url was clobbered"

[[ "$(field alice token_file)" == "secrets/hooks_token_alice" ]] \
  && pass "merge: token_file preserved" \
  || fail "merge: token_file was clobbered"

[[ "$(field alice peer_secret_file)" == "secrets/antenna-peer-alice.secret" ]] \
  && pass "merge: peer_secret_file preserved" \
  || fail "merge: peer_secret_file was clobbered"

[[ "$(field alice exchange_public_key)" == "age1original" ]] \
  && pass "merge: exchange_public_key preserved" \
  || fail "merge: exchange_public_key was clobbered"

# REF-604 spirit: unknown top-level peer-entry fields (e.g. .self from exchange)
# must survive a --force merge.
[[ "$(field alice self)" == "false" ]] \
  && pass "merge: unknown field .self preserved (REF-604 spirit)" \
  || fail "merge: unknown field .self was lost"

# ── Test 5: --force --exchange-public-key only merges, preserves everything else
run_peers_add alice --force --exchange-public-key age1rotated >/dev/null 2>&1 \
  && pass "force update alice --exchange-public-key: succeeded" \
  || fail "force update alice --exchange-public-key: should have succeeded"

[[ "$(field alice exchange_public_key)" == "age1rotated" ]] \
  && pass "merge: exchange_public_key updated" \
  || fail "merge: exchange_public_key not updated"

[[ "$(field alice display_name)" == "Alice (renamed)" ]] \
  && pass "merge: previously-merged display_name still preserved" \
  || fail "merge: display_name regressed"

[[ "$(field alice url)" == "https://alice.example" ]] \
  && pass "merge: url still preserved after second --force" \
  || fail "merge: url regressed"

[[ "$(field alice self)" == "false" ]] \
  && pass "merge: .self still preserved after second --force" \
  || fail "merge: .self regressed"

# ── Test 6: --force on a non-existent id still requires --url / --token-file ──
if run_peers_add dave --force --display-name "Dave" >/dev/null 2>&1; then
  fail "--force on new id without --url/--token-file should be refused"
else
  pass "--force on new id without --url/--token-file: refused"
fi

# ── Test 7: unknown option is still rejected ──────────────────────────────
if run_peers_add bob --force --bogus-flag >/dev/null 2>&1; then
  fail "unknown option should be rejected"
else
  pass "unknown option: rejected"
fi

# ── Summary ───────────────────────────────────────────────────────────────
echo ""
echo "── Summary ──"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
[[ $FAIL -eq 0 ]] || exit 1
