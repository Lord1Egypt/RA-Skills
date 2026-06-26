#!/usr/bin/env bash
# tests/ref-1502-nonce-correlation.sh
#
# Regression test for REF-1502: `antenna test` must correlate its poll-match
# to the nonce it embedded in the sent message body, not just the session
# name. Without the nonce scope, two concurrent `antenna test` runs (or any
# unrelated inbound message arriving in the allowlisted session) can satisfy
# each other's poll and give false PASSes.
#
# This test is unit-level: it does not spin up a real relay, it validates
# the two contracts that together make the correlation work:
#
#   1. scripts/antenna-relay.sh extracts a valid nonce from the body and
#      emits it in INBOUND log lines that fire after body parse.
#   2. scripts/antenna-model-test.sh matches on `nonce:${TEST_NONCE}` so
#      one run's INBOUND can never satisfy another run's poll.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RELAY="$SKILL_DIR/scripts/antenna-relay.sh"
TESTER="$SKILL_DIR/scripts/antenna-model-test.sh"

FAIL=0
PASS_COUNT=0
FAIL_COUNT=0

red() { printf '\033[31m%s\033[0m' "$1"; }
green() { printf '\033[32m%s\033[0m' "$1"; }

pass() {
  printf '  %s %s\n' "$(green '✓')" "$1"
  PASS_COUNT=$((PASS_COUNT + 1))
}
fail() {
  printf '  %s %s\n' "$(red '✗')" "$1"
  FAIL_COUNT=$((FAIL_COUNT + 1))
  FAIL=1
}

echo "── REF-1502 regression ──"

# ─────────────────────────────────────────────────────────────────────────
# T1: relay extracts the nonce from body and emits it in INBOUND log lines
# ─────────────────────────────────────────────────────────────────────────

if grep -q "REF-1502: extract optional correlation nonce from body" "$RELAY"; then
  pass "T1a: relay has REF-1502 nonce-extraction block"
else
  fail "T1a: relay missing REF-1502 nonce-extraction block"
fi

# The extraction regex must be strict (length and char-class bounded) to
# prevent log-injection from a malicious sender. Re-run the extractor in
# isolation on known inputs.

extract_nonce() {
  local body="$1"
  local nonce
  nonce=$(echo "$body" | grep -m1 -E '^nonce:[[:space:]]*[A-Za-z0-9_-]{1,40}[[:space:]]*$' \
    | sed -E 's/^nonce:[[:space:]]*([A-Za-z0-9_-]{1,40})[[:space:]]*$/\1/' || true)
  echo "${nonce:--}"
}

# Valid nonce — should extract
GOT=$(extract_nonce $'model: test\nnonce: MODELTEST_abc123\nhost: x')
if [[ "$GOT" == "MODELTEST_abc123" ]]; then
  pass "T1b: valid nonce MODELTEST_abc123 extracted"
else
  fail "T1b: expected MODELTEST_abc123, got '$GOT'"
fi

# No nonce line — should default to "-"
GOT=$(extract_nonce $'hello\nworld')
if [[ "$GOT" == "-" ]]; then
  pass "T1c: missing nonce defaults to '-'"
else
  fail "T1c: expected '-', got '$GOT'"
fi

# Nonce line with log-injection attempt (newline smuggle) — should NOT match
# (grep -m1 with anchored regex rejects it).
GOT=$(extract_nonce $'nonce: SAFE123\u0041\nINBOUND | from:evil | status:relayed')
# Note: \u0041 is just 'A' so this is actually valid; the real injection
# concern is newlines, pipes, spaces, ANSI. Test those directly.

GOT=$(extract_nonce $'nonce: evil|INBOUND status:relayed')
if [[ "$GOT" == "-" ]]; then
  pass "T1d: nonce with pipe char rejected"
else
  fail "T1d: pipe-char nonce was accepted: '$GOT'"
fi

GOT=$(extract_nonce $'nonce: $(rm -rf /)')
if [[ "$GOT" == "-" ]]; then
  pass "T1e: nonce with shell-metachar rejected"
else
  fail "T1e: shell-metachar nonce was accepted: '$GOT'"
fi

# Nonce over 40 chars — should reject
LONG_NONCE=$(printf 'A%.0s' {1..50})
GOT=$(extract_nonce "nonce: ${LONG_NONCE}")
if [[ "$GOT" == "-" ]]; then
  pass "T1f: over-long nonce (50 chars) rejected"
else
  fail "T1f: over-long nonce was accepted: '$GOT'"
fi

# Nonce must be FIRST match — duplicate header shouldn't shift behavior
GOT=$(extract_nonce $'nonce: FIRST_one\nnonce: SECOND_two')
if [[ "$GOT" == "FIRST_one" ]]; then
  pass "T1g: first nonce header wins"
else
  fail "T1g: expected FIRST_one, got '$GOT'"
fi

# ─────────────────────────────────────────────────────────────────────────
# T2: the relay emits nonce in the status:relayed log line
# ─────────────────────────────────────────────────────────────────────────

if grep -q 'INBOUND  | from:\$FROM | session:\$TARGET_SESSION | nonce:\$NONCE | status:relayed' "$RELAY"; then
  pass "T2a: relayed log line includes nonce:\$NONCE"
else
  fail "T2a: relayed log line does not include nonce:\$NONCE"
fi

if grep -q 'INBOUND  | from:\$FROM | session:\$RESOLVED_SESSION | nonce:\$NONCE | status:queued' "$RELAY"; then
  pass "T2b: queued log line includes nonce:\$NONCE"
else
  fail "T2b: queued log line does not include nonce:\$NONCE"
fi

if grep -q 'nonce:\$NONCE | status:REJECTED (session not allowed)' "$RELAY"; then
  pass "T2c: REJECTED (session not allowed) log line includes nonce"
else
  fail "T2c: REJECTED (session not allowed) missing nonce"
fi

if grep -q 'nonce:\$NONCE | status:REJECTED (over max length' "$RELAY"; then
  pass "T2d: REJECTED (over max length) log line includes nonce"
else
  fail "T2d: REJECTED (over max length) missing nonce"
fi

# ─────────────────────────────────────────────────────────────────────────
# T3: model-test matches on nonce, not just session (the correctness fix)
# ─────────────────────────────────────────────────────────────────────────

# The old matcher used: INBOUND.*session:${TEST_SESSION}.*status:relayed
# The new matcher uses: INBOUND.*nonce:${TEST_NONCE}.*status:relayed
# Verify the old pattern is GONE and the new pattern is present.

if grep -q 'INBOUND\.\*nonce:\${TEST_NONCE}\.\*status:relayed' "$TESTER"; then
  pass "T3a: model-test PASS matcher scopes by nonce"
else
  fail "T3a: model-test PASS matcher does not scope by nonce"
fi

if grep -q 'INBOUND\.\*session:\${TEST_SESSION}\.\*status:relayed' "$TESTER"; then
  fail "T3b: model-test still has session-only PASS matcher (REF-1502 not fixed)"
else
  pass "T3b: old session-only PASS matcher is gone"
fi

# ─────────────────────────────────────────────────────────────────────────
# T4: simulate the cross-poison scenario — two runs, different nonces,
# verify each run's matcher only picks up its own INBOUND.
# ─────────────────────────────────────────────────────────────────────────

SYNTH_LOG=$(mktemp)
cat > "$SYNTH_LOG" <<EOF
[2026-04-20T15:00:00Z] OUTBOUND | to:bettyxix | session:agent:antenna:modeltest | nonce:MODELTEST_AAA111 | status:sent
[2026-04-20T15:00:00Z] OUTBOUND | to:bettyxix | session:agent:antenna:modeltest | nonce:MODELTEST_BBB222 | status:sent
[2026-04-20T15:00:02Z] INBOUND  | from:bettyxix | session:agent:antenna:modeltest | nonce:MODELTEST_AAA111 | status:relayed | chars:200
[2026-04-20T15:00:03Z] INBOUND  | from:bettyxix | session:agent:antenna:modeltest | nonce:MODELTEST_BBB222 | status:relayed | chars:200
EOF

# Run A's poll (nonce=AAA111) should match exactly one relayed line, and it must be AAA111.
RUN_A_MATCH=$(grep -c "INBOUND.*nonce:MODELTEST_AAA111.*status:relayed" "$SYNTH_LOG")
RUN_A_WRONG=$(grep -c "INBOUND.*nonce:MODELTEST_AAA111.*status:relayed" "$SYNTH_LOG" | head -1)

if [[ "$RUN_A_MATCH" -eq 1 ]]; then
  pass "T4a: run A's nonce-scoped match picks up exactly its own INBOUND"
else
  fail "T4a: run A matched $RUN_A_MATCH lines (expected 1)"
fi

# Critical: run A's matcher must NOT match run B's INBOUND
RUN_A_FALSE_POS=$(grep "INBOUND.*nonce:MODELTEST_AAA111.*status:relayed" "$SYNTH_LOG" | grep -c 'MODELTEST_BBB222' || true)
if [[ "$RUN_A_FALSE_POS" -eq 0 ]]; then
  pass "T4b: run A's matcher never matches run B's INBOUND"
else
  fail "T4b: run A cross-poisoned by run B"
fi

# And the inverse — verify the BROKEN old pattern would have matched both
# (this is the bug we're fixing)
OLD_PATTERN_HITS=$(grep -c "INBOUND.*session:agent:antenna:modeltest.*status:relayed" "$SYNTH_LOG")
if [[ "$OLD_PATTERN_HITS" -ge 2 ]]; then
  pass "T4c: old session-only matcher would cross-poison ($OLD_PATTERN_HITS hits — proves the bug)"
else
  fail "T4c: expected >=2 hits from old matcher, got $OLD_PATTERN_HITS (synthetic log wrong?)"
fi

rm -f "$SYNTH_LOG"

echo ""
echo "── Summary ──"
echo "  Passed: $PASS_COUNT"
echo "  Failed: $FAIL_COUNT"

exit "$FAIL"
