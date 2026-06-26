#!/usr/bin/env bash
# REF-2001 regression test: `antenna doctor` surfaces malformed self-peer URLs.
#
# REF-1313 landed validate_peer_url into setup/exchange/CLI mutation paths,
# but doctor — the "did my install drift?" tool — still accepted any string
# in .self.url. This test locks down doctor's new behavior:
#
#   1. Self-peer URL is valid → pass line present, no "malformed" fail.
#   2. Self-peer URL is literally "main" (the devon1545 incident) → doctor
#      fails loud with the specific URL in the output.
#   3. Self-peer URL is missing → doctor fails with a "no URL configured"
#      signal (distinct from the malformed path).
#   4. A non-self peer with a malformed URL produces a warn line (not a
#      fail) so legacy installs aren't broken by the new check.
#
# We stop short of running doctor end-to-end: the gateway-config section
# and remote reachability calls are noisy/slow and irrelevant here. Instead
# we capture doctor's stdout/stderr and grep for the specific strings we
# own.
#
# Isolated SKILL_DIR; does not touch the live registry.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref2001-XXXXXX)"
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

# Minimal valid config so doctor doesn't bail early on other sections.
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

# Run doctor and capture combined output. We don't care about exit status
# here (doctor is a diagnostic tool and may exit non-zero for unrelated
# gateway-config concerns in the isolated test env).
run_doctor() {
  local out
  out="$(
    cd "$SKILL_DIR" && \
    SKILL_DIR="$SKILL_DIR" bash "$SKILL_DIR/scripts/antenna-doctor.sh" \
      --gateway "$SKILL_DIR/nonexistent-gateway.json" 2>&1
  )" || true
  printf '%s' "$out"
}

# ── Case 1: valid self URL ───────────────────────────────────────────────
echo "── REF-2001 case 1: valid self URL is acknowledged ─────────────────"
cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "testhost": {
    "self": true,
    "url": "https://testhost.example.com"
  }
}
JSON

out="$(run_doctor)"
if grep -qF "Self-peer URL looks valid: https://testhost.example.com" <<<"$out"; then
  pass "valid self URL produces the expected pass line"
else
  fail "valid self URL did not produce expected pass line" "$out"
fi
if grep -qF "Self-peer URL is malformed" <<<"$out"; then
  fail "valid self URL should NOT produce a malformed-URL fail line" "$out"
else
  pass "valid self URL did not produce a malformed-URL fail line"
fi

# ── Case 2: self URL is literally "main" (the devon1545 incident) ─────────
echo ""
echo "── REF-2001 case 2: self URL 'main' is caught ─────────────────────────"
cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "testhost": {
    "self": true,
    "url": "main"
  }
}
JSON

out="$(run_doctor)"
if grep -qF "Self-peer URL is malformed: main" <<<"$out"; then
  pass "self URL 'main' is reported as malformed"
else
  fail "self URL 'main' was not flagged" "$out"
fi

# ── Case 3: self URL missing entirely ────────────────────────────────────
echo ""
echo "── REF-2001 case 3: missing self URL is caught ────────────────────────"
cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "testhost": {
    "self": true
  }
}
JSON

out="$(run_doctor)"
if grep -qE "Self-peer.*has no URL configured" <<<"$out"; then
  pass "missing self URL is reported distinctly"
else
  fail "missing self URL was not flagged distinctly" "$out"
fi

# ── Case 4: other peer with malformed URL produces a warn, not a fail ────
echo ""
echo "── REF-2001 case 4: other peer's malformed URL is a warn ──────────────"
cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "testhost": {
    "self": true,
    "url": "https://testhost.example.com"
  },
  "legacy": {
    "url": "main"
  }
}
JSON

out="$(run_doctor)"
if grep -qF "Peers with malformed URLs: 1" <<<"$out"; then
  pass "non-self malformed URL surfaces as a warn line with count"
else
  fail "non-self malformed URL did not surface as expected" "$out"
fi
if grep -qE "✗.*Peers with malformed URLs" <<<"$out"; then
  fail "non-self malformed URL should be a warn, not a fail"
else
  pass "non-self malformed URL did not escalate to a fail"
fi

# ── Case 5: all peer URLs valid → affirmative pass line ──────────────────
echo ""
echo "── REF-2001 case 5: all peer URLs valid ───────────────────────────────"
cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "testhost": {
    "self": true,
    "url": "https://testhost.example.com"
  },
  "peer-ok": {
    "url": "https://peer-ok.example.com"
  }
}
JSON

out="$(run_doctor)"
if grep -qF "All peer URLs pass shape validation" <<<"$out"; then
  pass "affirmative pass line when all peer URLs are valid"
else
  fail "affirmative pass line missing when all peer URLs are valid" "$out"
fi

# ── Summary ──────────────────────────────────────────────────────────────
echo ""
echo "── REF-2001 summary ────────────────────────────────────────────────────"
echo "  passed: $PASS"
echo "  failed: $FAIL"
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
