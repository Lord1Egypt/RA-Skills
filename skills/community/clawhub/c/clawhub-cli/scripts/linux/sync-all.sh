#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF' >&2
Usage:
  sync-all.sh [--tags <tag>]... [--changelog <text>] [--bump patch|minor|major] [--dry-run]
EOF
}

tags=()
changelog=""
bump=""
dry_run=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tags) tags+=("${2:-}"); shift 2 ;;
    --changelog) changelog="${2:-}"; shift 2 ;;
    --bump) bump="${2:-}"; shift 2 ;;
    --dry-run) dry_run=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

args=(sync --all)

supports_flag() {
  local flag="$1"
  if ! command -v grep >/dev/null 2>&1; then
    return 1
  fi
  clawhub sync --help 2>/dev/null | grep -q -- "$flag"
}

if ((${#tags[@]} > 0)) && supports_flag "--tags"; then
  for t in "${tags[@]}"; do
    if [[ -n "$t" ]]; then
      args+=(--tags "$t")
    fi
  done
elif ((${#tags[@]} > 0)); then
  echo "!! Note: 'clawhub sync' does not appear to support '--tags' here. Ignoring tags." >&2
fi

if [[ -n "$changelog" ]] && supports_flag "--changelog"; then
  args+=(--changelog "$changelog")
elif [[ -n "$changelog" ]]; then
  echo "!! Note: 'clawhub sync' does not appear to support '--changelog' here. Ignoring changelog." >&2
fi

if [[ -n "$bump" ]] && supports_flag "--bump"; then
  args+=(--bump "$bump")
elif [[ -n "$bump" ]]; then
  echo "!! Note: 'clawhub sync' does not appear to support '--bump' here. Ignoring bump." >&2
fi

if $dry_run && supports_flag "--dry-run"; then
  args+=(--dry-run)
elif $dry_run; then
  echo "!! Note: 'clawhub sync' does not appear to support '--dry-run' here. Running without dry-run." >&2
fi

echo ">> clawhub ${args[*]}"
clawhub "${args[@]}"

