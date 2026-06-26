#!/usr/bin/env bash
set -euo pipefail

slug="${1:-}"
version="${2:-}"

if [[ -z "$slug" ]]; then
  echo "Usage: $0 <skill-slug> [semver]" >&2
  exit 2
fi

args=(install "$slug")
if [[ -n "$version" ]]; then
  args+=(--version "$version")
fi

echo ">> clawhub ${args[*]}"
clawhub "${args[@]}"

echo ">> clawhub list"
clawhub list

