#!/usr/bin/env bash
# REF-404 regression test: antenna-send must not silently fall back to hostname
# when the local self peer is missing from antenna-peers.json.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref404-XXXXXX)"
trap 'rm -rf "$TEST_ROOT"' EXIT

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  \033[31m✗\033[0m %s\n' "$1"; [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

echo "── REF-404 regression ──"

# 1. Static check: no hostname fallback remains in sender-identity resolution.
if awk '/# ── Build sender identity/,/REPLY_TO=/' "$SKILL_REPO/scripts/antenna-send.sh" \
  | grep -q 'Refusing to guess sender identity from hostname'; then
  pass "T1: sender identity path hard-fails instead of guessing hostname"
else
  fail "T1: sender identity path hard-fails instead of guessing hostname" "guard text not found"
fi

if awk '/# ── Build sender identity/,/REPLY_TO=/' "$SKILL_REPO/scripts/antenna-send.sh" \
  | grep -q 'hostname | tr'; then
  fail "T1b: hostname fallback removed from sender identity path" "hostname fallback still present"
else
  pass "T1b: hostname fallback removed from sender identity path"
fi

# 2. Live test in isolated skill dir: sending with no self peer should fail before curl.
SKILL_DIR="$TEST_ROOT/skill"
mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/lib" "$SKILL_DIR/secrets"
cp "$SKILL_REPO/scripts/antenna-send.sh" "$SKILL_DIR/scripts/"
cp -r "$SKILL_REPO/lib/." "$SKILL_DIR/lib/"

cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "max_message_length": 10000,
  "log_enabled": false,
  "allowed_outbound_peers": ["remote"],
  "default_target_session": "agent:betty:main"
}
JSON

cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "remote": {
    "url": "https://remote.example",
    "token_file": "secrets/hooks_token_remote",
    "agentId": "antenna"
  }
}
JSON

echo "remote-token" > "$SKILL_DIR/secrets/hooks_token_remote"
chmod 600 "$SKILL_DIR/secrets/hooks_token_remote"

# Stub curl so the test proves we fail before any network attempt.
mkdir -p "$TEST_ROOT/bin"
cat > "$TEST_ROOT/bin/curl" <<'BASH'
#!/usr/bin/env bash
echo "curl should not have been called" >&2
exit 99
BASH
chmod +x "$TEST_ROOT/bin/curl"

set +e
OUT="$(PATH="$TEST_ROOT/bin:$PATH" "$SKILL_DIR/scripts/antenna-send.sh" remote "hello" 2>&1)"
RC=$?
set -e

if [[ $RC -ne 0 ]] && grep -q 'Refusing to guess sender identity from hostname' <<<"$OUT"; then
  pass "T2: send fails loudly when self peer is missing"
else
  fail "T2: send fails loudly when self peer is missing" "rc=$RC output=$OUT"
fi

if [[ $RC -eq 99 ]] || grep -q 'curl should not have been called' <<<"$OUT"; then
  fail "T2b: sender aborts before network call" "curl stub was reached"
else
  pass "T2b: sender aborts before network call"
fi

echo
echo "── Summary ──"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]]
