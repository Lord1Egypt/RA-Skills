#!/usr/bin/env bash
# REF-2002 regression test: `antenna doctor` surfaces orphan peer references
# in antenna-config.json allowlists.
#
# REF-1312 taught `antenna peers remove` to prune allowlists, and REF-1313
# hardened URL validation on peer-add. What was still missing was the audit
# side: an operator whose config drifted before those fixes (or who hand-
# edited antenna-config.json) had no signal that `allowed_inbound_peers`,
# `allowed_outbound_peers`, or `inbox_auto_approve_peers` referenced peer
# IDs that no longer existed. This is the check that would have caught the
# pre-cleanup nexus / bruce debris automatically.
#
# Cases covered:
#   1. Clean config (no orphans) → affirmative pass line, no warn.
#   2. One orphan in `allowed_inbound_peers` → warn with count + the ID.
#   3. One orphan in `allowed_outbound_peers` → warn with count + the ID.
#   4. One orphan in `inbox_auto_approve_peers` → warn with count + the ID.
#   5. Multiple orphans across multiple lists → each field surfaces its
#      own warn and its own count.
#   6. Orphans are warns, never fails.
#   7. Missing fields are tolerated (no spurious warn when a field is
#      absent or empty).
#   8. Non-array field values do not crash the check.
#
# Isolated SKILL_DIR; does not touch the live registry.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref2002-XXXXXX)"
trap 'rm -rf "$TEST_ROOT"' EXIT

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() {
  FAIL=$((FAIL + 1))
  printf '  \033[31m✗\033[0m %s\n' "$1"
  [[ -n "${2:-}" ]] && printf '      %s\n' "$2"
}

# ── Build an isolated SKILL_DIR ──────────────────────────────────────────
SKILL_DIR="$TEST_ROOT/skill"
mkdir -p "$SKILL_DIR/bin" "$SKILL_DIR/lib" "$SKILL_DIR/scripts" "$SKILL_DIR/secrets"
cp "$SKILL_REPO/bin/antenna.sh" "$SKILL_DIR/bin/"
cp -r "$SKILL_REPO/lib/." "$SKILL_DIR/lib/"
cp -r "$SKILL_REPO/scripts/." "$SKILL_DIR/scripts/"

# Baseline peers file: a valid self-peer and two known non-self peers.
# Both self-URL and non-self URLs are valid so REF-2001 doesn't drown out
# our output with unrelated warns/fails.
cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "testhost": {
    "self": true,
    "url": "https://testhost.example.com"
  },
  "alice": {
    "url": "https://alice.example.com"
  },
  "bob": {
    "url": "https://bob.example.com"
  }
}
JSON

run_doctor() {
  local out
  out="$(
    cd "$SKILL_DIR" && \
    SKILL_DIR="$SKILL_DIR" bash "$SKILL_DIR/scripts/antenna-doctor.sh" \
      --gateway "$SKILL_DIR/nonexistent-gateway.json" 2>&1
  )" || true
  printf '%s' "$out"
}

# Extract the "1b. Peer-State Drift" section so case 1 assertions don't
# false-match on the "1. Antenna config" section above it.
extract_drift_section() {
  awk '/1b\. Peer-State Drift/,/^[0-9]+[a-z]?\. /' <<<"$1" \
    | sed -n '/1b\. Peer-State Drift/,/^2\. Gateway Configuration/p'
}

# ── Case 1: clean config, no orphans ─────────────────────────────────────
echo "── REF-2002 case 1: clean allowlists produce pass, no warn ────────────"
cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "self_id": "testhost",
  "display_name": "Test Host",
  "relay_agent_model": "unset",
  "allowed_inbound_peers": ["alice", "bob"],
  "allowed_outbound_peers": ["alice"],
  "inbox_auto_approve_peers": ["bob"],
  "allowed_inbound_sessions": []
}
JSON

out="$(run_doctor)"
drift="$(extract_drift_section "$out")"

if grep -qF "No orphan peer references in config allowlists" <<<"$drift"; then
  pass "clean config produces affirmative pass line"
else
  fail "clean config did not produce the affirmative pass line" "$drift"
fi
if grep -qE "references unknown peer" <<<"$drift"; then
  fail "clean config should NOT produce any orphan warn lines" "$drift"
else
  pass "clean config produced no orphan warn lines"
fi

# ── Case 2: orphan in allowed_inbound_peers ──────────────────────────────
echo ""
echo "── REF-2002 case 2: orphan in allowed_inbound_peers is caught ─────────"
cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "self_id": "testhost",
  "allowed_inbound_peers": ["alice", "nexus"],
  "allowed_outbound_peers": ["alice"],
  "inbox_auto_approve_peers": [],
  "allowed_inbound_sessions": []
}
JSON

out="$(run_doctor)"
drift="$(extract_drift_section "$out")"

if grep -qF "allowed_inbound_peers references unknown peer(s): 1" <<<"$drift"; then
  pass "orphan in allowed_inbound_peers produces warn with count"
else
  fail "orphan in allowed_inbound_peers was not reported" "$drift"
fi
if grep -qE -- "- nexus" <<<"$drift"; then
  pass "orphan ID 'nexus' appears in hint lines"
else
  fail "orphan ID 'nexus' missing from output" "$drift"
fi

# ── Case 3: orphan in allowed_outbound_peers ─────────────────────────────
echo ""
echo "── REF-2002 case 3: orphan in allowed_outbound_peers is caught ────────"
cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "self_id": "testhost",
  "allowed_inbound_peers": ["alice"],
  "allowed_outbound_peers": ["alice", "bruce"],
  "inbox_auto_approve_peers": [],
  "allowed_inbound_sessions": []
}
JSON

out="$(run_doctor)"
drift="$(extract_drift_section "$out")"

if grep -qF "allowed_outbound_peers references unknown peer(s): 1" <<<"$drift"; then
  pass "orphan in allowed_outbound_peers produces warn with count"
else
  fail "orphan in allowed_outbound_peers was not reported" "$drift"
fi
if grep -qE -- "- bruce" <<<"$drift"; then
  pass "orphan ID 'bruce' appears in hint lines"
else
  fail "orphan ID 'bruce' missing from output" "$drift"
fi

# ── Case 4: orphan in inbox_auto_approve_peers ───────────────────────────
echo ""
echo "── REF-2002 case 4: orphan in inbox_auto_approve_peers is caught ──────"
cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "self_id": "testhost",
  "allowed_inbound_peers": ["alice"],
  "allowed_outbound_peers": ["alice"],
  "inbox_auto_approve_peers": ["ghost"],
  "allowed_inbound_sessions": []
}
JSON

out="$(run_doctor)"
drift="$(extract_drift_section "$out")"

if grep -qF "inbox_auto_approve_peers references unknown peer(s): 1" <<<"$drift"; then
  pass "orphan in inbox_auto_approve_peers produces warn with count"
else
  fail "orphan in inbox_auto_approve_peers was not reported" "$drift"
fi
if grep -qE -- "- ghost" <<<"$drift"; then
  pass "orphan ID 'ghost' appears in hint lines"
else
  fail "orphan ID 'ghost' missing from output" "$drift"
fi

# ── Case 5: multiple orphans across multiple lists ───────────────────────
echo ""
echo "── REF-2002 case 5: multiple orphans in multiple lists ────────────────"
cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "self_id": "testhost",
  "allowed_inbound_peers": ["alice", "nexus", "zombie"],
  "allowed_outbound_peers": ["bruce"],
  "inbox_auto_approve_peers": ["ghost", "phantom"],
  "allowed_inbound_sessions": []
}
JSON

out="$(run_doctor)"
drift="$(extract_drift_section "$out")"

if grep -qF "allowed_inbound_peers references unknown peer(s): 2" <<<"$drift"; then
  pass "allowed_inbound_peers reports count 2"
else
  fail "allowed_inbound_peers count was not 2" "$drift"
fi
if grep -qF "allowed_outbound_peers references unknown peer(s): 1" <<<"$drift"; then
  pass "allowed_outbound_peers reports count 1"
else
  fail "allowed_outbound_peers count was not 1" "$drift"
fi
if grep -qF "inbox_auto_approve_peers references unknown peer(s): 2" <<<"$drift"; then
  pass "inbox_auto_approve_peers reports count 2"
else
  fail "inbox_auto_approve_peers count was not 2" "$drift"
fi

# ── Case 6: orphans are warns, not fails ─────────────────────────────────
echo ""
echo "── REF-2002 case 6: orphans are warns, not fails ──────────────────────"
# Re-run doctor with the case-5 config (still on disk).
out="$(run_doctor)"
drift="$(extract_drift_section "$out")"

if grep -qE "✗.*references unknown peer" <<<"$drift"; then
  fail "orphan reference should never be a fail line" "$drift"
else
  pass "no orphan reference produced a fail line"
fi
if grep -qE "⚠.*references unknown peer" <<<"$drift"; then
  pass "orphan references use the warn glyph"
else
  fail "orphan references did not use the warn glyph" "$drift"
fi

# ── Case 7: missing / empty fields are tolerated ─────────────────────────
echo ""
echo "── REF-2002 case 7: missing / empty fields do not produce warns ───────"
cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "self_id": "testhost"
}
JSON

out="$(run_doctor)"
drift="$(extract_drift_section "$out")"

if grep -qE "references unknown peer" <<<"$drift"; then
  fail "missing allowlist fields should not produce warns" "$drift"
else
  pass "missing allowlist fields produced no warns"
fi
if grep -qF "No orphan peer references in config allowlists" <<<"$drift"; then
  pass "missing fields still produce the affirmative pass line"
else
  fail "missing fields did not produce the affirmative pass line" "$drift"
fi

# ── Case 8: non-array field value does not crash ─────────────────────────
echo ""
echo "── REF-2002 case 8: non-array field values don't crash the check ──────"
cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "self_id": "testhost",
  "allowed_inbound_peers": "not-an-array",
  "allowed_outbound_peers": null,
  "inbox_auto_approve_peers": 42
}
JSON

out="$(run_doctor)"
drift="$(extract_drift_section "$out")"

# Should not crash, should not falsely report orphans from the garbage values.
if grep -qE "references unknown peer" <<<"$drift"; then
  fail "non-array field values should not produce orphan warns" "$drift"
else
  pass "non-array field values were treated as empty"
fi
if grep -qF "No orphan peer references in config allowlists" <<<"$drift"; then
  pass "non-array fields still produce the affirmative pass line"
else
  fail "non-array fields did not produce the affirmative pass line" "$drift"
fi

# ── Summary ──────────────────────────────────────────────────────────────
echo ""
echo "── REF-2002 summary ───────────────────────────────────────────────────"
echo "  passed: $PASS"
echo "  failed: $FAIL"
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
