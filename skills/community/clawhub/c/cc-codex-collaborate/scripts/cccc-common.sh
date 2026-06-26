#!/usr/bin/env bash
# Shared helpers for cc-codex-collaborate.
set -euo pipefail

cccc_repo_root() {
  git rev-parse --show-toplevel 2>/dev/null || pwd
}

cccc_root() {
  echo "docs/cccc"
}

cccc_state() {
  echo "docs/cccc/state.json"
}

cccc_config() {
  echo "docs/cccc/config.json"
}

cccc_skill_dir() {
  local root
  root="$(cccc_repo_root)"
  echo "$root/.claude/skills/cc-codex-collaborate"
}

cccc_now() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

cccc_require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 127
  fi
}

cccc_init_dirs() {
  mkdir -p docs/cccc/{reviews/plan,reviews/milestones,logs,runtime,templates,backups}
}

# Read a value from config.json. Usage: cccc_config_value '.mode' 'default'
cccc_config_value() {
  local key="$1" default="$2"
  local config
  config="$(cccc_config)"
  if [[ -f "$config" ]]; then
    python3 - "$config" "$key" "$default" <<'PY'
import json, sys
try:
    data = json.loads(open(sys.argv[1]).read())
    parts = sys.argv[2].lstrip('.').split('.')
    v = data
    for p in parts:
        if isinstance(v, dict) and p in v:
            v = v[p]
        else:
            v = None
            break
    print(v if v is not None else sys.argv[3])
except Exception:
    print(sys.argv[3])
PY
  else
    echo "$default"
  fi
}
