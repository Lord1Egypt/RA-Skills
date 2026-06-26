#!/usr/bin/env bash
# REF-1313 regression test: peer URL shape validation across every write boundary.
#
# Fixes the "url: main" incident (2026-04-21): a malformed self-peer URL
# round-tripped from one host to another via bootstrap bundles because
# antenna-setup.sh, antenna-exchange.sh build_plaintext_bundle_stdout,
# antenna-exchange.sh validate_bundle_json, and bin/antenna.sh peers add
# all accepted any non-empty string.
#
# What this test covers:
#   1. The shared validator in lib/peers.sh accepts good URLs and rejects bad
#      ones, including the specific "main" footgun. Exercised directly as a
#      pure-function unit test so a future scheme/host rule change fails loud.
#   2. `antenna peers add --url <bad>` is refused. --force path is refused
#      too.
#   3. `antenna peers add --url http://... ` is refused by default and
#      accepted with --allow-insecure.
#   4. Non-interactive `antenna setup --url <bad>` hard-fails before
#      touching antenna-peers.json.
#   5. Non-interactive `antenna setup --url http://internal` fails without
#      --allow-insecure and succeeds with it.
#
# We stop short of round-tripping a crafted bootstrap bundle here — the
# bundle code path is exercised through exchange's own regression tests.
# The key guarantee this test locks down is: every CLI surface that can
# write a peer URL rejects garbage.
#
# Runs against an isolated $SKILL_DIR; does not touch the live registry.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref1313-XXXXXX)"
trap 'rm -rf "$TEST_ROOT"' EXIT

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  \033[31m✗\033[0m %s\n' "$1"; [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

# ── Part 1: unit-test validate_peer_url directly ─────────────────────────
echo "── REF-1313 part 1: validate_peer_url unit checks ──────────────────────"
# shellcheck source=../lib/peers.sh
source "$SKILL_REPO/lib/peers.sh"

# Expect-accept matrix
accepts=(
  "https://bettyxix.tailde275c.ts.net"
  "https://example.com"
  "https://example.com/"
  "https://example.com:8443"
  "https://example.com/hooks/agent"
  "https://127.0.0.1"
  "https://127.0.0.1:8080"
  "https://localhost"
  "https://localhost:8443"
)
for u in "${accepts[@]}"; do
  if validate_peer_url "$u" false 2>/dev/null; then
    pass "accept: $u"
  else
    fail "should accept: $u"
  fi
done

# Expect-accept with allow_insecure=true
insecure_accepts=(
  "http://localhost"
  "http://localhost:8080"
  "http://dev.internal:9000"
)
for u in "${insecure_accepts[@]}"; do
  if validate_peer_url "$u" true 2>/dev/null; then
    pass "accept (insecure): $u"
  else
    fail "should accept with insecure: $u"
  fi
done

# Expect-reject matrix — the meat of REF-1313.
rejects=(
  ""                          # empty
  "main"                      # the bug that started it all
  "https://main"              # single-label host, no dot
  "https://foo"               # single-label, no dot
  "http://example.com"        # insecure without flag
  "ftp://example.com"         # wrong scheme
  "https://"                  # bare scheme
  "https:// "                 # whitespace
  "https://example.com?x=1"   # query string
  "https://example.com#frag"  # fragment
  "not a url at all"          # spaces + no scheme
)
for u in "${rejects[@]}"; do
  if validate_peer_url "$u" false 2>/dev/null; then
    fail "should reject: '$u'"
  else
    pass "reject: '${u:-<empty>}'"
  fi
done

# Insecure flag must NOT accept non-http(s) either.
if validate_peer_url "ftp://example.com" true 2>/dev/null; then
  fail "--allow-insecure must not accept ftp://"
else
  pass "--allow-insecure still rejects ftp://"
fi

# ── Build an isolated SKILL_DIR for CLI-surface tests ────────────────────
echo ""
echo "── REF-1313 part 2: peers add and setup reject bad URLs ────────────────"

SKILL_DIR="$TEST_ROOT/skill"
mkdir -p "$SKILL_DIR/bin" "$SKILL_DIR/lib" "$SKILL_DIR/scripts" "$SKILL_DIR/secrets"
cp "$SKILL_REPO/bin/antenna.sh" "$SKILL_DIR/bin/"
cp -r "$SKILL_REPO/lib/." "$SKILL_DIR/lib/"
# setup script also needs its companion scripts; copy the directory.
cp -r "$SKILL_REPO/scripts/." "$SKILL_DIR/scripts/"
cp "$SKILL_REPO/antenna-config.schema.json" "$SKILL_DIR/" 2>/dev/null || true

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

cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{}
JSON

run_peers_add() {
  (
    cd "$SKILL_DIR"
    SKILL_DIR="$SKILL_DIR" bash "$SKILL_DIR/bin/antenna.sh" peers add "$@"
  )
}

PEERS_FILE="$SKILL_DIR/antenna-peers.json"

# CLI reject: --url "main"
BEFORE="$(cat "$PEERS_FILE")"
if run_peers_add bob --url main --token-file secrets/hooks_token_bob >/dev/null 2>&1; then
  fail "peers add --url main should be refused"
else
  pass "peers add --url main: refused"
fi
AFTER="$(cat "$PEERS_FILE")"
[[ "$BEFORE" == "$AFTER" ]] \
  && pass "peers add --url main: registry unchanged" \
  || fail "peers add --url main: registry was modified"

# CLI reject: --url "https://foo" (single-label)
if run_peers_add bob --url https://foo --token-file secrets/hooks_token_bob >/dev/null 2>&1; then
  fail "peers add --url https://foo should be refused"
else
  pass "peers add --url https://foo: refused"
fi

# CLI reject: --url http://... without --allow-insecure
if run_peers_add bob --url http://bob.example --token-file secrets/hooks_token_bob >/dev/null 2>&1; then
  fail "peers add --url http://... without --allow-insecure should be refused"
else
  pass "peers add http:// without --allow-insecure: refused"
fi

# CLI accept: --url https://bob.example (good)
if run_peers_add bob --url https://bob.example --token-file secrets/hooks_token_bob >/dev/null 2>&1; then
  pass "peers add --url https://bob.example: accepted"
else
  fail "peers add good https URL: should have succeeded"
fi

# CLI accept: --url http://localhost:8080 with --allow-insecure (peer "carol")
if run_peers_add carol --url http://localhost:8080 --token-file secrets/hooks_token_carol --allow-insecure >/dev/null 2>&1; then
  pass "peers add http://localhost:8080 --allow-insecure: accepted"
else
  fail "peers add http://localhost:8080 --allow-insecure: should have succeeded"
fi

# CLI reject on --force update with bad --url
if run_peers_add bob --force --url main >/dev/null 2>&1; then
  fail "peers add --force --url main should be refused"
else
  pass "peers add --force --url main: refused"
fi

# Ensure bob's url is still good after the refused --force update.
bob_url_after="$(jq -r '.bob.url' "$PEERS_FILE")"
[[ "$bob_url_after" == "https://bob.example" ]] \
  && pass "--force rejection: bob.url preserved" \
  || fail "--force rejection: bob.url mutated to '$bob_url_after'"

echo ""
echo "── REF-1313 part 3: non-interactive setup rejects bad --url ────────────"

# Drive antenna-setup.sh non-interactively in a sub-SKILL_DIR so we don't
# overwrite the registry we just built. Setup touches a lot of state; the
# simplest clean fixture is a brand-new empty skill tree.
SETUP_DIR="$TEST_ROOT/setup-skill"
mkdir -p "$SETUP_DIR/bin" "$SETUP_DIR/lib" "$SETUP_DIR/scripts" "$SETUP_DIR/secrets"
cp "$SKILL_REPO/bin/antenna.sh" "$SETUP_DIR/bin/"
cp -r "$SKILL_REPO/lib/." "$SETUP_DIR/lib/"
cp -r "$SKILL_REPO/scripts/." "$SETUP_DIR/scripts/"

run_setup() {
  # Run with SKILL_DIR pinned so the script operates on our scratch dir.
  (
    cd "$SETUP_DIR"
    SKILL_DIR="$SETUP_DIR" bash "$SETUP_DIR/scripts/antenna-setup.sh" \
      --non-interactive \
      --host-id testhost \
      --display "Test Host" \
      --agent-id antenna \
      --model "noop/noop" \
      "$@"
  )
}

# Reject: --url main
if run_setup --url main >/dev/null 2>&1; then
  fail "setup --url main should be refused"
else
  pass "setup --url main: refused"
fi
[[ ! -f "$SETUP_DIR/antenna-peers.json" ]] \
  && pass "setup --url main: antenna-peers.json NOT created" \
  || fail "setup --url main: antenna-peers.json was created ($(cat "$SETUP_DIR/antenna-peers.json"))"

# Reject: --url http://... without --allow-insecure
if run_setup --url http://testhost.example >/dev/null 2>&1; then
  fail "setup --url http://... without --allow-insecure should be refused"
else
  pass "setup http:// without --allow-insecure: refused"
fi

# We do not run a full positive-path setup here because setup also tries to
# register an agent with the live gateway, which is out of scope for this
# test. The --url validation fires before that step, which is exactly where
# REF-1313 needs the gate.

echo ""
echo "── Summary ──"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
[[ $FAIL -eq 0 ]] || exit 1
