#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF' >&2
Usage:
  update all:
    update-skills.sh --all

  update one:
    update-skills.sh --slug <skill-slug> [--version <semver>]
EOF
}

all=false
slug=""
version=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) all=true; shift ;;
    --slug) slug="${2:-}"; shift 2 ;;
    --version) version="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

if $all; then
  echo ">> clawhub update --all"
  clawhub update --all
elif [[ -n "$slug" ]]; then
  args=(update "$slug")
  if [[ -n "$version" ]]; then
    args+=(--version "$version")
  fi
  echo ">> clawhub ${args[*]}"
  clawhub "${args[@]}"
else
  echo "Provide --all or --slug <skill-slug>." >&2
  usage
  exit 2
fi

echo ">> clawhub list"
clawhub list

