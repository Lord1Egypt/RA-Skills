#!/usr/bin/env bash
set -euo pipefail

skill_folder="${1:-}"
slug="${2:-}"
name="${3:-}"
version="${4:-}"
tags_csv="${5:-latest}"

if [[ -z "$skill_folder" || -z "$slug" || -z "$name" || -z "$version" ]]; then
  echo "Usage: $0 <skill-folder> <slug> <display-name> <semver> [tags_csv]" >&2
  echo "Example: $0 ./skills/my-skill my-skill \"My Skill\" 0.1.0 latest,beta" >&2
  exit 2
fi

IFS=',' read -r -a tags <<<"$tags_csv"

supports_flag() {
  local cmd="$1"
  local flag="$2"
  if ! command -v grep >/dev/null 2>&1; then
    return 1
  fi
  clawhub "$cmd" --help 2>/dev/null | grep -q -- "$flag"
}

args=(publish "$skill_folder" --slug "$slug" --name "$name" --version "$version")
if supports_flag "publish" "--tags"; then
  for t in "${tags[@]}"; do
    if [[ -n "$t" ]]; then
      args+=(--tags "$t")
    fi
  done
else
  echo "!! Note: 'clawhub publish' does not appear to support '--tags' in this environment. Publishing without tags." >&2
fi

echo ">> clawhub ${args[*]}"
clawhub "${args[@]}"

