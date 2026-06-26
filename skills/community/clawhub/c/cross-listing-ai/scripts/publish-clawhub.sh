#!/usr/bin/env bash
set -euo pipefail

main() {
  local version=${1-}
  local changelog=${2-}
  local tags=${3-}
  local script_dir repo_root
  local -a publish_command required_files

  script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
  repo_root=$(cd "$script_dir/.." && pwd)
  required_files=()
  while IFS= read -r required_file; do
    required_files+=("$required_file")
  done < <(build_required_files "$repo_root")

  if [[ -z "$version" ]]; then
    usage >&2
    exit 1
  fi

  require_files "$repo_root" "${required_files[@]}"
  require_clean_git "$repo_root"
  require_command "clawhub"

  publish_command=(
    "clawhub"
    "publish"
    "$repo_root"
    "--slug"
    "cross-listing-ai"
    "--name"
    "Cross Listing AI"
    "--version"
    "$version"
  )

  if [[ -n "$changelog" ]]; then
    publish_command+=("--changelog" "$changelog")
  fi

  if [[ -n "$tags" ]]; then
    publish_command+=("--tags" "$tags")
  fi

  if ! (cd "$repo_root" && "${publish_command[@]}"); then
    echo "ClawHub publish failed. If authentication is the problem, run 'clawhub login' and retry." >&2
    exit 1
  fi
}

usage() {
  cat <<'EOF'
Usage: scripts/publish-clawhub.sh <version> [changelog] [tags]

Publishes the current repo contents to ClawHub.
EOF
}

build_required_files() {
  local repo_root=$1

  printf '%s\n' "README.md" "SKILL.md" "LICENSE" "agents/openai.yaml"
  (
    cd "$repo_root"
    grep -Eo 'references/[A-Za-z0-9./-]+\.md' SKILL.md | sort -u
  )
}

require_files() {
  local repo_root=$1
  shift

  local relative_path
  for relative_path in "$@"; do
    if [[ ! -f "$repo_root/$relative_path" ]]; then
      echo "Missing required file: $relative_path" >&2
      exit 1
    fi
  done
}

require_clean_git() {
  local repo_root=$1

  if [[ -n "$(git -C "$repo_root" status --short)" ]]; then
    echo "This publish flow requires a clean git working tree." >&2
    exit 1
  fi
}

require_command() {
  local command_name=$1

  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing required command: $command_name" >&2
    exit 1
  fi
}

main "$@"
