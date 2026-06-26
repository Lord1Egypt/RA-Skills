#!/usr/bin/env bash
# REF-2000 regression test: `antenna bundle verify` shape/freshness check.
#
# This locks down the operator-facing bundle verifier so shape, URL, and
# freshness checks stay aligned with what scripts/antenna-exchange.sh
# enforces during real imports. Without this test it would be very easy
# to let the `antenna bundle verify` output silently drift from the
# import path (e.g. someone adds a field to the bundle and forgets to
# teach one of the two validators).
#
# We run exclusively through `--no-decrypt` so the test never depends on
# a local age key or on age being set up correctly — decryption itself
# is covered by existing exchange regressions. What we care about here
# is that, given plaintext JSON, the verifier:
#
#   1. Accepts a well-formed, fresh bundle (exit 0, ok=true).
#   2. Rejects a malformed schema_version (exit 1, shape reason).
#   3. Rejects a bundle whose from_endpoint_url is "main" — the
#      devon1545 incident (REF-1313). Locks in that the verifier
#      is using the shared validator, not a soft string check.
#   4. Rejects an expired bundle, and accepts it with --force-expired.
#   5. Never leaks the token / identity secret into the output. This is
#      the only place we care about that invariant at shell level, so
#      it's cheap to assert here.
#   6. Missing files return a distinct exit code path (not 0).
#   7. --json output is parseable and has the expected top-level shape
#      (ok, file, reasons, summary with no sensitive fields).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref2000-XXXXXX)"
trap 'rm -rf "$TEST_ROOT"' EXIT

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() {
  FAIL=$((FAIL + 1))
  printf '  \033[31m✗\033[0m %s\n' "$1"
  [[ -n "${2:-}" ]] && printf '      %s\n' "$2"
}

# ── Fixtures ────────────────────────────────────────────────────────────
#
# Everything is an in-memory JSON file under $TEST_ROOT. We never run age.

# Sentinel values we look for when asserting "sensitive fields not printed".
SENTINEL_TOKEN="TOK3N_SENTINEL_f00dcafe"
SENTINEL_SECRET="deadbeef$(printf 'a%.0s' {1..56})"  # 64-char hex-ish

write_bundle() {
  local path="$1" expires="$2" url="$3" schema="${4:-1}"
  cat > "$path" <<JSON
{
  "schema_version": $schema,
  "bundle_type": "antenna-bootstrap",
  "generated_at": "2099-01-01T00:00:00Z",
  "expires_at": "$expires",
  "bundle_id": "test-bundle-id",
  "from_peer_id": "testpeer",
  "from_display_name": "Test Peer",
  "from_endpoint_url": "$url",
  "from_agent_id": "antenna",
  "from_hooks_token": "$SENTINEL_TOKEN",
  "from_identity_secret": "$SENTINEL_SECRET",
  "from_exchange_pubkey": "age1abcdefghijklmnopqrstuvwxyzabcdef",
  "expected_peer_id": null,
  "notes": null
}
JSON
}

GOOD="$TEST_ROOT/good.json"
BAD_SCHEMA="$TEST_ROOT/bad-schema.json"
BAD_URL="$TEST_ROOT/bad-url.json"
EXPIRED="$TEST_ROOT/expired.json"

write_bundle "$GOOD"        "2099-12-31T23:59:59Z" "https://test.example.com"
write_bundle "$BAD_SCHEMA"  "2099-12-31T23:59:59Z" "https://test.example.com" 2
write_bundle "$BAD_URL"     "2099-12-31T23:59:59Z" "main"
write_bundle "$EXPIRED"     "2000-01-01T00:00:00Z" "https://test.example.com"

ANTENNA="$SKILL_REPO/bin/antenna.sh"

# Helper to run verify and capture stdout+stderr together, plus exit code.
run_verify() {
  local out rc
  out=$(bash "$ANTENNA" bundle verify "$@" 2>&1)
  rc=$?
  printf '%s\n' "$out"
  return $rc
}

printf '── REF-2000: antenna bundle verify ─────────────────────────────\n'
printf '  TEST_ROOT=%s\n\n' "$TEST_ROOT"

# ── T1: valid bundle → exit 0 ───────────────────────────────────────────
out=$(run_verify "$GOOD" --no-decrypt); rc=$?
if [[ $rc -eq 0 ]]; then
  pass "T1: valid bundle accepted (exit 0)"
else
  fail "T1: valid bundle should exit 0, got $rc" "$out"
fi

# T1b: no sensitive fields leaked to human output
if grep -q "$SENTINEL_TOKEN" <<<"$out"; then
  fail "T1b: hooks token leaked into human output"
else
  pass "T1b: hooks token not printed in human output"
fi
if grep -q "$SENTINEL_SECRET" <<<"$out"; then
  fail "T1b: identity secret leaked into human output"
else
  pass "T1b: identity secret not printed in human output"
fi

# T1c: key positive markers present
if grep -q 'Bundle verification passed' <<<"$out" \
   && grep -q 'Shape OK' <<<"$out" \
   && grep -q 'Bundle is fresh' <<<"$out"; then
  pass "T1c: positive summary markers present"
else
  fail "T1c: missing expected positive markers" "$out"
fi

# ── T2: malformed schema_version → fail ─────────────────────────────────
out=$(run_verify "$BAD_SCHEMA" --no-decrypt); rc=$?
if [[ $rc -eq 1 ]]; then
  pass "T2: bad schema_version → exit 1"
else
  fail "T2: bad schema_version should exit 1, got $rc" "$out"
fi
if grep -q 'schema_version must be 1' <<<"$out"; then
  pass "T2: specific schema_version reason emitted"
else
  fail "T2: expected 'schema_version must be 1' reason" "$out"
fi

# ── T3: malformed URL (devon1545 "main" regression) ─────────────────────
out=$(run_verify "$BAD_URL" --no-decrypt); rc=$?
if [[ $rc -eq 1 ]]; then
  pass "T3: from_endpoint_url='main' → exit 1"
else
  fail "T3: bad URL should exit 1, got $rc" "$out"
fi
if grep -q 'Endpoint URL invalid' <<<"$out"; then
  pass "T3: endpoint URL rejection message emitted"
else
  fail "T3: expected 'Endpoint URL invalid' message" "$out"
fi

# ── T4: expired bundle → fail by default, pass with --force-expired ─────
out=$(run_verify "$EXPIRED" --no-decrypt); rc=$?
if [[ $rc -eq 1 ]]; then
  pass "T4a: expired bundle → exit 1"
else
  fail "T4a: expired bundle should exit 1, got $rc" "$out"
fi
if grep -q 'expired' <<<"$out"; then
  pass "T4a: expired reason surfaced"
else
  fail "T4a: expected 'expired' in output" "$out"
fi

out=$(run_verify "$EXPIRED" --no-decrypt --force-expired); rc=$?
if [[ $rc -eq 0 ]]; then
  pass "T4b: expired + --force-expired → exit 0"
else
  fail "T4b: --force-expired should exit 0, got $rc" "$out"
fi
if grep -q -- '--force-expired' <<<"$out"; then
  pass "T4b: warning mentions --force-expired override"
else
  fail "T4b: expected --force-expired mention in warning" "$out"
fi

# ── T5: missing file ────────────────────────────────────────────────────
out=$(run_verify "$TEST_ROOT/does-not-exist.age.txt"); rc=$?
if [[ $rc -eq 1 ]]; then
  pass "T5: missing file → exit 1"
else
  fail "T5: missing file should exit 1, got $rc" "$out"
fi
if grep -q 'File not found' <<<"$out"; then
  pass "T5: 'File not found' message emitted"
else
  fail "T5: expected 'File not found' in output" "$out"
fi

# ── T6: --json shape and secrets-not-leaked ─────────────────────────────
out=$(run_verify "$GOOD" --no-decrypt --json); rc=$?
if [[ $rc -eq 0 ]]; then
  pass "T6: --json exit 0 on valid bundle"
else
  fail "T6: --json should exit 0, got $rc" "$out"
fi
if jq -e 'type == "object" and has("ok") and has("file") and has("reasons") and has("summary")' <<<"$out" >/dev/null 2>&1; then
  pass "T6: --json output has expected top-level shape"
else
  fail "T6: --json output missing required keys" "$out"
fi
if jq -e '.summary | has("has_hooks_token") and has("has_identity_secret")' <<<"$out" >/dev/null 2>&1; then
  pass "T6: summary exposes has_* signals (not raw values)"
else
  fail "T6: summary missing has_hooks_token/has_identity_secret" "$out"
fi
# Critical: JSON output must NOT contain the actual token or secret.
if grep -q "$SENTINEL_TOKEN" <<<"$out"; then
  fail "T6: hooks token leaked in --json output"
else
  pass "T6: hooks token not present in --json output"
fi
if grep -q "$SENTINEL_SECRET" <<<"$out"; then
  fail "T6: identity secret leaked in --json output"
else
  pass "T6: identity secret not present in --json output"
fi

# T6b: --json on failure still emits parseable JSON with ok=false + reasons
out=$(run_verify "$BAD_URL" --no-decrypt --json); rc=$?
if [[ $rc -eq 1 ]]; then
  pass "T6b: --json failure → exit 1"
else
  fail "T6b: --json failure should exit 1, got $rc" "$out"
fi
if jq -e '.ok == false and (.reasons | length > 0)' <<<"$out" >/dev/null 2>&1; then
  pass "T6b: --json failure reports ok=false with reasons[]"
else
  fail "T6b: --json failure JSON not shaped as expected" "$out"
fi

# ── Summary ─────────────────────────────────────────────────────────────
echo
echo "── REF-2000 summary ────────────────────────────────────────────────"
echo "  passed: $PASS"
echo "  failed: $FAIL"
[[ $FAIL -eq 0 ]] || exit 1
exit 0
