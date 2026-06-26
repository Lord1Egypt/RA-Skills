#!/usr/bin/env bash
# REF-903 regression test: setup reruns must not silently strip an operator's
# custom tools.exec policy from an existing antenna agent.
#
# Structural coverage only. This validates the jq update path in
# scripts/antenna-setup.sh preserves tools.exec while still forcing sandbox off
# and seeding default tools.deny when absent.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
SETUP="$SKILL_REPO/scripts/antenna-setup.sh"

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  \033[31m✗\033[0m %s\n' "$1"; [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

echo "── REF-903 regression ──"

UPDATE_BLOCK="$(awk '/Antenna agent already registered in gateway config/,/# 4\) Enable cross-agent session visibility/' "$SETUP")"

# T1: legacy destructive delete is gone.
if printf '%s\n' "$UPDATE_BLOCK" | grep -q 'del(.exec)'; then
  fail "T1: setup update path no longer deletes tools.exec" "found destructive del(.exec) in antenna agent repair path"
else
  pass "T1: setup update path no longer deletes tools.exec"
fi

# T2: repair path still forces sandbox off.
if printf '%s\n' "$UPDATE_BLOCK" | grep -q '.sandbox = { mode: "off" }'; then
  pass "T2: setup update path still forces sandbox.mode=off"
else
  fail "T2: setup update path still forces sandbox.mode=off" "sandbox repair assignment not found"
fi

# T3: repair path normalizes non-object .tools without clobbering real objects.
if printf '%s\n' "$UPDATE_BLOCK" | grep -q '.tools = (if (.tools | type) == "object" then .tools else {} end)'; then
  pass "T3: setup update path preserves existing tools object"
else
  fail "T3: setup update path preserves existing tools object" "expected object-preserving .tools normalization not found"
fi

# T4: default deny list is only seeded when absent.
if printf '%s\n' "$UPDATE_BLOCK" | grep -q '.tools.deny = (.tools.deny // \['; then
  pass "T4: setup only seeds tools.deny defaults when absent"
else
  fail "T4: setup only seeds tools.deny defaults when absent" "expected // defaulting pattern for tools.deny not found"
fi

# T5: live jq seam, operator tools.exec survives repair.
TEST_JSON='{
  "agents": {
    "list": [
      {
        "id": "antenna",
        "sandbox": {},
        "tools": {
          "exec": { "security": "deny", "ask": "always" },
          "deny": ["custom:one"]
        }
      }
    ]
  }
}'

PATCHED="$(printf '%s\n' "$TEST_JSON" | jq '
  .agents.list = [.agents.list[] |
    if .id == "antenna" then
      .sandbox = { mode: "off" } |
      .tools = (if (.tools | type) == "object" then .tools else {} end) |
      .tools.deny = (.tools.deny // [
        "group:web", "browser", "image", "image_generate",
        "cron", "memory_search", "memory_get",
        "web_search", "web_fetch"
      ])
    else . end
  ]
')"

if [[ "$(printf '%s\n' "$PATCHED" | jq -r '.agents.list[0].tools.exec.security')" == "deny" ]] \
   && [[ "$(printf '%s\n' "$PATCHED" | jq -r '.agents.list[0].tools.exec.ask')" == "always" ]]; then
  pass "T5: live repair jq preserves operator tools.exec policy"
else
  fail "T5: live repair jq preserves operator tools.exec policy" "operator tools.exec values were altered"
fi

# T6: live jq seam, existing deny list is preserved.
if [[ "$(printf '%s\n' "$PATCHED" | jq -r '.agents.list[0].tools.deny[0]')" == "custom:one" ]]; then
  pass "T6: live repair jq preserves operator tools.deny entries"
else
  fail "T6: live repair jq preserves operator tools.deny entries" "existing deny list was overwritten"
fi

# T7: live jq seam, missing deny list is seeded.
NO_DENY='{
  "agents": {
    "list": [
      {
        "id": "antenna",
        "sandbox": {},
        "tools": {
          "exec": { "security": "allowlist" }
        }
      }
    ]
  }
}'

PATCHED_NO_DENY="$(printf '%s\n' "$NO_DENY" | jq '
  .agents.list = [.agents.list[] |
    if .id == "antenna" then
      .sandbox = { mode: "off" } |
      .tools = (if (.tools | type) == "object" then .tools else {} end) |
      .tools.deny = (.tools.deny // [
        "group:web", "browser", "image", "image_generate",
        "cron", "memory_search", "memory_get",
        "web_search", "web_fetch"
      ])
    else . end
  ]
')"

if [[ "$(printf '%s\n' "$PATCHED_NO_DENY" | jq -r '.agents.list[0].tools.deny[0]')" == "group:web" ]]; then
  pass "T7: live repair jq seeds default deny list only when absent"
else
  fail "T7: live repair jq seeds default deny list only when absent" "default deny list was not added"
fi

echo
echo "── Summary ──"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]]
