#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
UNINSTALL_SCRIPT="$SKILL_DIR/scripts/antenna-uninstall.sh"

pass() { printf 'PASS  %s\n' "$*"; }
fail() { printf 'FAIL  %s\n' "$*" >&2; exit 1; }

assert_no_antenna() {
  local file="$1" label="$2"
  local remaining
  remaining="$(jq '[
    (if (.agents | type) == "array" then .agents[] else empty end),
    (if (.agents | type) == "object" then (if (.agents.list | type) == "array" then .agents.list[] else empty end) else empty end),
    (if (.agents | type) == "object" then (if (.agents.entries | type) == "object" then .agents.entries[] else empty end) else empty end),
    (if (.agents | type) == "object" then (.agents[] | select(type == "object" and .id? != null)) else empty end)
  ] | map(select((.id // "") == "antenna" or ((.name // "") | ascii_downcase) == "antenna relay")) | length' "$file")"
  [[ "$remaining" == "0" ]] || fail "$label: antenna agent still present"
}

assert_hooks_clean() {
  local file="$1" label="$2"
  jq -e '
    ((.hooks.allowedAgentIds // []) | index("antenna")) == null and
    ((.hooks.allowedSessionKeyPrefixes // []) | index("hook:antenna")) == null
  ' "$file" >/dev/null || fail "$label: hooks entries still present"
}

run_case() {
  local name="$1" json="$2"
  local tmpdir gateway skill
  tmpdir="$(mktemp -d /tmp/ref1200-XXXXXX)"
  skill="$tmpdir/skill"
  gateway="$tmpdir/openclaw.json"
  mkdir -p "$skill/scripts"
  cp "$UNINSTALL_SCRIPT" "$skill/scripts/antenna-uninstall.sh"
  printf '%s\n' "$json" > "$gateway"
  HOME="$tmpdir/home" USER=tester bash "$skill/scripts/antenna-uninstall.sh" --yes --dry-run --gateway "$gateway" >/dev/null
  HOME="$tmpdir/home" USER=tester bash "$skill/scripts/antenna-uninstall.sh" --yes --gateway "$gateway" >/dev/null
  assert_no_antenna "$gateway" "$name"
  assert_hooks_clean "$gateway" "$name"
  rm -rf "$tmpdir"
  pass "$name"
}

run_case "agents.list shape" '{
  "agents": {
    "defaults": {"model": "x"},
    "list": [
      {"id": "main", "name": "Main Agent"},
      {"id": "antenna", "name": "Antenna Relay"}
    ]
  },
  "hooks": {
    "allowedAgentIds": ["main", "antenna"],
    "allowedSessionKeyPrefixes": ["hook:antenna", "hook:other"]
  }
}'

run_case "agents array shape" '{
  "agents": [
    {"id": "main", "name": "Main Agent"},
    {"id": "antenna", "name": "Antenna Relay"}
  ],
  "hooks": {
    "allowedAgentIds": ["antenna"],
    "allowedSessionKeyPrefixes": ["hook:antenna"]
  }
}'

run_case "agents.entries shape" '{
  "agents": {
    "entries": {
      "main": {"id": "main", "name": "Main Agent"},
      "antenna": {"id": "antenna", "name": "Antenna Relay"}
    }
  },
  "hooks": {
    "allowedAgentIds": ["antenna", "main"],
    "allowedSessionKeyPrefixes": ["hook:antenna", "hook:main"]
  }
}'

echo "All REF-1200 uninstall cleanup tests passed."
