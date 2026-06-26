#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_HOME="${CODEX_HOME:-$HOME/.codex}/skills"
CATALOG_PATH="$SKILL_ROOT/config/dependency-sources.json"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/self-heal-local-dependency.sh <dependency>
  bash scripts/self-heal-local-dependency.sh <dependency>

Supported dependencies:
  agent-spectrum
  resonance-contract
  tomorrowdao-agent-skills
  portkey-ca-agent-skills
  all
EOF
}

get_catalog_field() {
  local dep="$1"
  local field="$2"
  python3 - "$CATALOG_PATH" "$dep" "$field" <<'PY'
import json
import sys
from pathlib import Path

catalog = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
dep = sys.argv[2]
field = sys.argv[3]
entry = catalog["dependencies"].get(dep)
if not entry:
    raise SystemExit(1)
value = entry.get(field, "")
if value is None:
    value = ""
print(value)
PY
}

resolve_local_skill_path() {
  local root="$1"
  local skill_subdir="$2"
  if [[ -e "$root/$skill_subdir" ]]; then
    printf '%s\n' "$root/$skill_subdir"
    return 0
  fi
  if [[ "$skill_subdir" != "." && -e "$root/SKILL.md" ]]; then
    printf '%s\n' "$root"
    return 0
  fi
  if [[ "$skill_subdir" == "." && -e "$root" ]]; then
    printf '%s\n' "$root"
    return 0
  fi
  return 1
}

clone_repo_source() {
  local repo_url="$1"
  local workdir="$2"
  if ! command -v git >/dev/null 2>&1; then
    echo "[self-heal] git is required for repo-based install or upgrade: $repo_url" >&2
    return 1
  fi
  git clone --depth 1 "$repo_url" "$workdir/repo" >/dev/null 2>&1 || {
    echo "[self-heal] failed to clone dependency source repo: $repo_url" >&2
    return 1
  }
  printf '%s\n' "$workdir/repo"
}

render_source_summary() {
  local dep="$1"
  local repo_url="$2"
  local env_name="$3"
  local env_value="${!env_name:-}"
  if [[ -n "$env_value" ]]; then
    printf '%s\n' "$env_name=$env_value"
    return 0
  fi
  printf '%s\n' "$repo_url"
}

install_or_refresh_one() {
  local dep="$1"
  local repo_url env_name skill_subdir min_version
  repo_url="$(get_catalog_field "$dep" default_repo_url)"
  env_name="$(get_catalog_field "$dep" env_override)"
  skill_subdir="$(get_catalog_field "$dep" skill_subdir)"
  min_version="$(get_catalog_field "$dep" min_version)"
  local target="$SKILLS_HOME/$dep"
  local source_path=""
  local source_root=""
  local temp_dir
  local env_value="${!env_name:-}"

  temp_dir="$(mktemp -d)"

  if [[ -n "$env_value" ]]; then
    if source_root="$(resolve_local_skill_path "$env_value" "$skill_subdir" 2>/dev/null)"; then
      source_path="$source_root"
    else
      echo "[self-heal] warning: $env_name points to an unusable local source, falling back to $repo_url" >&2
    fi
  fi

  if [[ -z "$source_path" ]]; then
    source_root="$(clone_repo_source "$repo_url" "$temp_dir")" || {
      rm -rf "$temp_dir"
      return 1
    }
    source_path="$(resolve_local_skill_path "$source_root" "$skill_subdir")" || {
      echo "[self-heal] could not resolve skill subdir '$skill_subdir' inside $repo_url" >&2
      rm -rf "$temp_dir"
      return 1
    }
  fi

  mkdir -p "$SKILLS_HOME"
  local temp_target="$SKILLS_HOME/.${dep}.tmp.$$"
  rm -rf "$temp_target"
  mkdir -p "$temp_target"
  cp -R "$source_path"/. "$temp_target"/
  rm -rf "$target"
  mv "$temp_target" "$target"
  echo "[self-heal] installed or upgraded $dep (minimum version: $min_version) from $(render_source_summary "$dep" "$repo_url" "$env_name")"
  rm -rf "$temp_dir"
  return 0
}

main() {
  local dep="${1:-}"
  if [[ -z "$dep" ]]; then
    usage >&2
    exit 1
  fi

  if [[ "$dep" == "all" ]]; then
    install_or_refresh_one agent-spectrum
    install_or_refresh_one resonance-contract
    install_or_refresh_one tomorrowdao-agent-skills
    install_or_refresh_one portkey-ca-agent-skills
    exit 0
  fi

  install_or_refresh_one "$dep"
}

main "$@"
