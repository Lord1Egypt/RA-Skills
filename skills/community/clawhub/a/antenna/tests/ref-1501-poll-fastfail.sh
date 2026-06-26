#!/usr/bin/env bash
# REF-1501 regression: auth/peer/rate-limit REJECTED log lines must carry the
# nonce so antenna-model-test's nonce-scoped fast-fail loop catches them
# without burning the full --timeout.
#
# Fixture-free: we source relay.sh at module-level is not safe, so we grep
# the source for the specific log_entry call shapes and run narrow end-to-end
# checks using fake envelopes against a stubbed environment.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
RELAY="$SKILL_DIR/scripts/antenna-relay.sh"
MODEL_TEST="$SKILL_DIR/scripts/antenna-model-test.sh"

PASS=0
FAIL=0
ok()  { echo "  $(printf '\033[32m✓\033[0m') $*"; PASS=$((PASS+1)); }
bad() { echo "  $(printf '\033[31m✗\033[0m') $*"; FAIL=$((FAIL+1)); }

echo "── T1: relay log_entry lines for pre-body REJECTED paths carry nonce ──"

# The two envelope-marker MALFORMED paths genuinely cannot carry nonce
# (body hasn't been parsed yet). Everything else MUST.
declare -a EXPECTED_WITH_NONCE=(
  "status:REJECTED \(missing from\)"
  "status:REJECTED \(not in allowed_inbound_peers\)"
  "status:REJECTED \(unknown peer\)"
  "status:REJECTED \(peer secret file missing\)"
  "status:REJECTED \(missing auth header\)"
  "status:REJECTED \(invalid peer secret\)"
  "status:REJECTED \(rate limited: peer"
  "status:REJECTED \(rate limited: global"
  "status:REJECTED \(session not allowed\)"
  "status:REJECTED \(over max length:"
  "status:relayed"
  "status:queued"
)

for pat in "${EXPECTED_WITH_NONCE[@]}"; do
  # Find log_entry lines matching the pattern; verify nonce:$NONCE is present
  matches=$(grep -E "log_entry .*${pat}" "$RELAY" || true)
  if [[ -z "$matches" ]]; then
    bad "no log_entry found for: ${pat}"
    continue
  fi
  missing=0
  while IFS= read -r line; do
    if ! grep -q 'nonce:\$NONCE' <<< "$line"; then
      missing=1
      echo "     offender: $line"
    fi
  done <<< "$matches"
  if [[ $missing -eq 0 ]]; then
    ok "nonce on: ${pat}"
  else
    bad "missing nonce on one or more lines: ${pat}"
  fi
done

echo ""
echo "── T2: envelope-marker MALFORMED paths are exempt (pre-body) ──"

if grep -q 'log_entry "INBOUND  | status:MALFORMED (no envelope markers)"' "$RELAY"; then
  ok "no-envelope MALFORMED stays nonce-less (pre-body)"
else
  bad "expected no-envelope MALFORMED log_entry not found"
fi

if grep -q 'log_entry "INBOUND  | status:MALFORMED (no closing marker)"' "$RELAY"; then
  ok "no-closing-marker MALFORMED stays nonce-less (pre-body)"
else
  bad "expected no-closing MALFORMED log_entry not found"
fi

echo ""
echo "── T3: model-test poll loop has nonce-scoped REJECTED fast-fail ──"

if grep -Eq 'INBOUND.*nonce:\$\{TEST_NONCE\}.*status:REJECTED' "$MODEL_TEST"; then
  ok "model-test fast-fails on nonce-scoped REJECTED"
else
  bad "model-test missing nonce-scoped REJECTED fast-fail in poll loop"
fi

echo ""
echo "── T4: end-to-end — auth-failure REJECTED arrives with our nonce ──"

# Build a minimal envelope with a bogus sender; relay will reject because
# peer is unknown. That line must include our nonce.
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

NONCE="REF1501_$(date +%s%N | sha256sum | cut -c1-10)"
# Use a live timestamp so REF-402 freshness check passes; we want to exercise
# the peer-allowlist REJECTED path (which is what REF-1501 is about), not the
# timestamp-too-old path.
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ENV="[ANTENNA_RELAY]
from: totally-not-a-real-peer-$RANDOM
target_session: agent:betty:main
timestamp: ${NOW}

nonce: ${NONCE}
hello from test
[/ANTENNA_RELAY]"

# Point the relay at a scratch config/peers so we don't touch real state.
SCRATCH_LOG="$TMP/relay.log"
SCRATCH_CFG="$TMP/config.json"
SCRATCH_PEERS="$TMP/peers.json"
cat > "$SCRATCH_CFG" <<JSON
{"log_path":"$SCRATCH_LOG","log_enabled":"true","allowed_inbound_peers":["bettyxix"],"allowed_inbound_sessions":["agent:betty:main"]}
JSON
cat > "$SCRATCH_PEERS" <<'JSON'
{"bettyxix":{"self":true,"url":"http://localhost"}}
JSON

# Shim SKILL_DIR-relative paths by setting CONFIG_FILE/PEERS_FILE via env
# override (relay.sh computes these from SCRIPT_DIR). Instead we copy the
# scratch files into the real file paths the relay derives.
#
# Simpler: use bash -c with a minimal harness that overrides CONFIG_FILE
# after sourcing — but relay.sh exec's as a script. So run the relay as a
# subprocess with PWD unchanged and rely on default config; we only care
# that the REJECTED line carries nonce, and we can compare against the
# real config's allowlist. If our from: isn't allowed, we get REJECTED.

# Run against the real config; pick a guaranteed-unknown peer name.
OUT=$(bash "$RELAY" "$ENV" 2>&1 || true)

LOG_FILE=$(bash -c 'cd "$1" && source lib/config.sh; CONFIG_FILE="$1/antenna-config.json"; echo "$(config_log_path)"' _ "$SKILL_DIR")
if [[ "$LOG_FILE" != /* ]]; then
  LOG_FILE="$SKILL_DIR/$LOG_FILE"
fi

# Grep the last few log lines for our nonce+REJECTED
RECENT=$(tail -20 "$LOG_FILE" 2>/dev/null || true)
if echo "$RECENT" | grep -qE "INBOUND.*nonce:${NONCE}.*status:REJECTED"; then
  ok "auth-failure REJECTED carries our nonce in live log"
else
  bad "auth-failure REJECTED did not carry our nonce"
  echo "     recent log tail:"
  echo "$RECENT" | sed 's/^/       /'
fi

echo ""
echo "── Summary ──"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
[[ $FAIL -eq 0 ]]
