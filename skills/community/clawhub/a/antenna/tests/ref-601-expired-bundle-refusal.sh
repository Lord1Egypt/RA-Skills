#!/usr/bin/env bash
# REF-601 regression test: expired encrypted bootstrap bundles are refused by default.
#
# Layers under test:
#   1. validate_bundle_json requires a valid expires_at field.
#   2. validate_bundle_freshness refuses expired bundles by default.
#   3. --force-expired is present as an intentional escape hatch.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref601-XXXXXX)"
trap 'rm -rf "$TEST_ROOT"' EXIT

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  \033[31m✗\033[0m %s\n' "$1"; [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

echo "── REF-601 regression ──"

# 1. Static check: validate_bundle_json delegates shape validation to the
# shared bundle helper, and that helper requires expires_at format.
if awk '/^validate_bundle_json\(\) \{/,/^\}/' "$SKILL_REPO/scripts/antenna-exchange.sh" \
    | grep -q 'bundle_shape_reason' \
  && awk '/^bundle_shape_reason\(\) \{/,/^\}/' "$SKILL_REPO/lib/bundles.sh" \
    | grep -q 'expires_at'; then
  pass "T1: validate_bundle_json delegates expires_at shape validation"
else
  fail "T1: validate_bundle_json delegates expires_at shape validation" "delegated expires_at validation not found"
fi

# 2. Static check: validate_bundle_freshness exists and compares against now.
if awk '/^validate_bundle_freshness\(\) \{/,/^\}/' "$SKILL_REPO/scripts/antenna-exchange.sh" \
  | grep -Fq ".expires_at >= \$now"; then
  pass "T2: validate_bundle_freshness rejects expired bundles"
else
  fail "T2: validate_bundle_freshness rejects expired bundles" "freshness comparison missing"
fi

# 3. Live seam test: source the helpers, create an expired bundle JSON, ensure default refusal.

BUNDLE_JSON="$TEST_ROOT/expired-bundle.json"
cat > "$BUNDLE_JSON" <<'JSON'
{
  "schema_version": 1,
  "bundle_type": "antenna-bootstrap",
  "generated_at": "2026-01-01T00:00:00Z",
  "expires_at": "2026-01-02T00:00:00Z",
  "bundle_id": "deadbeefdeadbeefdeadbeef",
  "from_peer_id": "remotepeer",
  "from_display_name": "Remote Peer",
  "from_endpoint_url": "https://remote.example",
  "from_agent_id": "antenna",
  "from_hooks_token": "token123",
  "from_identity_secret": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "from_exchange_pubkey": "age1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqs7f8v"
}
JSON

HARNESS="$TEST_ROOT/harness.sh"
cat > "$HARNESS" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
die() { echo "$1" >&2; exit "${2:-1}"; }
BUNDLE_JSON="$1"
SKILL_REPO="$2"
SKILL_DIR="$SKILL_REPO"
# shellcheck source=/dev/null
source "$SKILL_REPO/lib/peers.sh"
# shellcheck source=/dev/null
source "$SKILL_REPO/lib/bundles.sh"
# shellcheck source=/dev/null
source <(awk '
  /^now_iso\(\) \{/ , /^\}/ { print }
  /^validate_bundle_json\(\) \{/ , /^\}/ { print }
  /^validate_bundle_freshness\(\) \{/ , /^\}/ { print }
' "$SKILL_REPO/scripts/antenna-exchange.sh")
validate_bundle_json "$BUNDLE_JSON"
validate_bundle_freshness "$BUNDLE_JSON" false
BASH
chmod +x "$HARNESS"

set +e
OUT="$($HARNESS "$BUNDLE_JSON" "$SKILL_REPO" 2>&1)"
RC=$?
set -e
if [[ $RC -ne 0 ]] && grep -q 'Bundle expired at' <<<"$OUT"; then
  pass "T3: expired bundle is refused by default"
else
  fail "T3: expired bundle is refused by default" "rc=$RC output=$OUT"
fi

# 4. Live seam test: --force-expired path allows deliberate override.
HARNESS_FORCE="$TEST_ROOT/harness-force.sh"
cat > "$HARNESS_FORCE" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
die() { echo "$1" >&2; exit "${2:-1}"; }
BUNDLE_JSON="$1"
SKILL_REPO="$2"
SKILL_DIR="$SKILL_REPO"
# shellcheck source=/dev/null
source "$SKILL_REPO/lib/peers.sh"
# shellcheck source=/dev/null
source "$SKILL_REPO/lib/bundles.sh"
# shellcheck source=/dev/null
source <(awk '
  /^now_iso\(\) \{/ , /^\}/ { print }
  /^validate_bundle_json\(\) \{/ , /^\}/ { print }
  /^validate_bundle_freshness\(\) \{/ , /^\}/ { print }
' "$SKILL_REPO/scripts/antenna-exchange.sh")
validate_bundle_json "$BUNDLE_JSON"
validate_bundle_freshness "$BUNDLE_JSON" true
BASH
chmod +x "$HARNESS_FORCE"

if "$HARNESS_FORCE" "$BUNDLE_JSON" "$SKILL_REPO" >/dev/null 2>&1; then
  pass "T4: force_expired override allows deliberate import"
else
  fail "T4: force_expired override allows deliberate import"
fi

# 5. Static check: CLI exposes --force-expired on import.
if grep -q -- '--force-expired' "$SKILL_REPO/scripts/antenna-exchange.sh"; then
  pass "T5: CLI documents and parses --force-expired"
else
  fail "T5: CLI documents and parses --force-expired" "option not found"
fi

echo
echo "── Summary ──"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]]
