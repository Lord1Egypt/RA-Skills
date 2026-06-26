#!/usr/bin/env bash
set -euo pipefail

main() {
  local script_dir repo_root
  local -a required_files

  script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
  repo_root=$(cd "$script_dir/.." && pwd)
  required_files=()
  while IFS= read -r required_file; do
    required_files+=("$required_file")
  done < <(build_required_files "$repo_root")

  require_files "$repo_root" "${required_files[@]}"
  require_clean_git "$repo_root"
  require_origin_main_matches_head "$repo_root"
  require_command "npx"

  (
    cd "$repo_root"
    npx skills check
  )

  cat <<'EOF'
skills.sh uses the pushed default branch as the install target for this repo.
Verified target: origin/main
Share/install target: AryanJ-NYC/cross-listing-ai
Install command: npx skills add AryanJ-NYC/cross-listing-ai
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

require_origin_main_matches_head() {
  local repo_root=$1
  local current_branch head_sha origin_main_sha

  current_branch=$(git -C "$repo_root" branch --show-current)
  if [[ "$current_branch" != "main" ]]; then
    echo "skills.sh publish must run from the local main branch after pushing origin/main." >&2
    exit 1
  fi

  if ! git -C "$repo_root" rev-parse --verify origin/main >/dev/null 2>&1; then
    echo "Missing remote tracking branch: origin/main" >&2
    exit 1
  fi

  head_sha=$(git -C "$repo_root" rev-parse HEAD)
  origin_main_sha=$(git -C "$repo_root" rev-parse origin/main)
  if [[ "$head_sha" != "$origin_main_sha" ]]; then
    echo "skills.sh publish requires local HEAD to match origin/main. Push or update main first." >&2
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
