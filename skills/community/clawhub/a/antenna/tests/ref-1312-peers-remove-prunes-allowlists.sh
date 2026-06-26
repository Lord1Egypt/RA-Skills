#!/usr/bin/env bash
# REF-1312 regression test: `antenna peers remove <id>` prunes peer-scoped
# allowlists in antenna-config.json, not just the registry entry.
#
# Pre-REF-1312 bug: removing a peer left stale references in
#   - allowed_inbound_peers
#   - allowed_outbound_peers
#   - inbox_auto_approve_peers
# That leftover state meant a future peer with the same id would silently
# inherit trust the operator thought they had cleared. Surfaced live during
# the 2026-04-21 'bruce' / 'nexus' cleanup.
#
# Guarantees under test:
#   1. `peers remove` deletes the registry entry (unchanged behavior).
#   2. `peers remove` removes the id from allowed_inbound_peers.
#   3. `peers remove` removes the id from allowed_outbound_peers.
#   4. `peers remove` removes the id from inbox_auto_approve_peers.
#   5. `peers remove` does NOT touch allowed_inbound_sessions (those are
#      session strings, not peer ids — a session key that happens to match
#      the peer id must survive because it could be unrelated).
#   6. `peers remove` on an id that's in the allowlists but NOT in the
#      registry still prunes the allowlists (clean up orphans).
#   7. Other peers in those same allowlists are untouched.
#
# Runs against an isolated $SKILL_DIR; does not touch the live registry.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref1312-XXXXXX)"
trap 'rm -rf "$TEST_ROOT"' EXIT

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  \033[31m✗\033[0m %s\n' "$1"; [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

# ── Build isolated SKILL_DIR ─────────────────────────────────────────────
SKILL_DIR="$TEST_ROOT/skill"
mkdir -p "$SKILL_DIR/bin" "$SKILL_DIR/lib" "$SKILL_DIR/secrets"
cp "$SKILL_REPO/bin/antenna.sh" "$SKILL_DIR/bin/"
cp -r "$SKILL_REPO/lib/." "$SKILL_DIR/lib/"
cp "$SKILL_REPO/antenna-config.schema.json" "$SKILL_DIR/" 2>/dev/null || true

# Config: two peers in each peer-scoped allowlist + a session-string that
# coincidentally matches the peer id we'll remove (to lock in that session
# allowlists are NOT touched).
cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "self_id": "testhost",
  "display_name": "Test Host",
  "relay_agent_model": "unset",
  "allowed_inbound_peers": ["alice", "bob", "carol"],
  "allowed_outbound_peers": ["alice", "bob"],
  "allowed_inbound_sessions": ["agent:antenna:main", "bob", "agent:betty:main"],
  "inbox_auto_approve_peers": ["bob", "carol"]
}
JSON

cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "alice": {
    "url": "https://alice.example",
    "token_file": "secrets/hooks_token_alice",
    "agentId": "antenna",
    "display_name": "Alice"
  },
  "bob": {
    "url": "https://bob.example",
    "token_file": "secrets/hooks_token_bob",
    "agentId": "antenna",
    "display_name": "Bob"
  },
  "carol": {
    "url": "https://carol.example",
    "token_file": "secrets/hooks_token_carol",
    "agentId": "antenna",
    "display_name": "Carol"
  }
}
JSON

run_peers() {
  (
    cd "$SKILL_DIR"
    SKILL_DIR="$SKILL_DIR" bash "$SKILL_DIR/bin/antenna.sh" peers "$@"
  )
}

CONFIG="$SKILL_DIR/antenna-config.json"
PEERS="$SKILL_DIR/antenna-peers.json"

has_in_array() {
  # has_in_array <jq-path-expr> <value> -> echoes "true" / "false"
  jq -r --arg v "$2" "($1) | index(\$v) != null" "$CONFIG"
}

echo "── REF-1312: peers remove prunes peer-scoped allowlists ────────────────"
echo ""

# Sanity check: bob is where we expect before we remove.
[[ "$(has_in_array '.allowed_inbound_peers'     'bob')" == "true" ]] || { fail "precondition: bob missing from allowed_inbound_peers"; }
[[ "$(has_in_array '.allowed_outbound_peers'    'bob')" == "true" ]] || { fail "precondition: bob missing from allowed_outbound_peers"; }
[[ "$(has_in_array '.inbox_auto_approve_peers'  'bob')" == "true" ]] || { fail "precondition: bob missing from inbox_auto_approve_peers"; }
[[ "$(has_in_array '.allowed_inbound_sessions'  'bob')" == "true" ]] || { fail "precondition: bob session placeholder missing"; }

# ── Remove bob ────────────────────────────────────────────────────────────
run_peers remove bob >/dev/null 2>&1 \
  && pass "peers remove bob: exited 0" \
  || fail "peers remove bob: exited non-zero"

# Registry entry gone
[[ "$(jq -r 'has("bob")' "$PEERS")" == "false" ]] \
  && pass "registry: bob deleted" \
  || fail "registry: bob still present"

# Peer-scoped allowlists pruned
[[ "$(has_in_array '.allowed_inbound_peers'     'bob')" == "false" ]] \
  && pass "allowed_inbound_peers: bob pruned" \
  || fail "allowed_inbound_peers: bob still present"

[[ "$(has_in_array '.allowed_outbound_peers'    'bob')" == "false" ]] \
  && pass "allowed_outbound_peers: bob pruned" \
  || fail "allowed_outbound_peers: bob still present"

[[ "$(has_in_array '.inbox_auto_approve_peers'  'bob')" == "false" ]] \
  && pass "inbox_auto_approve_peers: bob pruned" \
  || fail "inbox_auto_approve_peers: bob still present"

# Session allowlist explicitly NOT touched
[[ "$(has_in_array '.allowed_inbound_sessions'  'bob')" == "true" ]] \
  && pass "allowed_inbound_sessions: 'bob' entry preserved (sessions are not peer ids)" \
  || fail "allowed_inbound_sessions: 'bob' was removed — REF-1312 must not touch session allowlist"

# Other peers untouched
[[ "$(has_in_array '.allowed_inbound_peers'  'alice')" == "true" ]] \
  && pass "other peers: alice still in allowed_inbound_peers" \
  || fail "other peers: alice was collateral-damaged"

[[ "$(has_in_array '.allowed_outbound_peers' 'alice')" == "true" ]] \
  && pass "other peers: alice still in allowed_outbound_peers" \
  || fail "other peers: alice was collateral-damaged"

[[ "$(has_in_array '.inbox_auto_approve_peers' 'carol')" == "true" ]] \
  && pass "other peers: carol still in inbox_auto_approve_peers" \
  || fail "other peers: carol was collateral-damaged"

# ── Orphan cleanup: remove an id that's in allowlists but NOT registry ──
# Simulate a stale allowlist entry for a peer that was already removed.
tmp=$(mktemp)
jq '.allowed_inbound_peers += ["ghost"] | .allowed_outbound_peers += ["ghost"]' "$CONFIG" > "$tmp" && mv "$tmp" "$CONFIG"

run_peers remove ghost >/dev/null 2>&1 \
  && pass "peers remove ghost (orphan): exited 0" \
  || fail "peers remove ghost (orphan): exited non-zero"

[[ "$(has_in_array '.allowed_inbound_peers'  'ghost')" == "false" ]] \
  && pass "orphan cleanup: ghost pruned from allowed_inbound_peers" \
  || fail "orphan cleanup: ghost still in allowed_inbound_peers"

[[ "$(has_in_array '.allowed_outbound_peers' 'ghost')" == "false" ]] \
  && pass "orphan cleanup: ghost pruned from allowed_outbound_peers" \
  || fail "orphan cleanup: ghost still in allowed_outbound_peers"

echo ""
echo "── Summary ──"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
[[ $FAIL -eq 0 ]] || exit 1
