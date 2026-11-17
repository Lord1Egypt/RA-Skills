#!/usr/bin/env bash
set -euo pipefail

ARENA_REEXEC="${ARENA_REEXEC:-0}"

skill_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
expected_repo='yagel-yosef/arena-skill'
expected_url="https://github.com/$expected_repo.git"
repo_root="$(git -C "$skill_dir" rev-parse --show-toplevel 2>/dev/null || true)"

# ClawHub publishes regular skill files without Git metadata. Fetch the same
# source repository and replace only the files this skill owns in that case.
if [[ "$repo_root" != "$skill_dir" ]]; then
  temp_dir="$(mktemp -d)"
  trap 'rm -rf -- "$temp_dir"' EXIT
  GIT_TERMINAL_PROMPT=0 git clone --quiet --depth 1 --branch main "$expected_url" "$temp_dir/arena"

  files=(SKILL.md README.md scripts/update.sh)
  changed=false
  for file in "${files[@]}"; do
    source_file="$temp_dir/arena/$file"
    if [[ ! -f "$source_file" || -L "$source_file" ]]; then
      printf 'Arena update stopped: missing or linked source file %s.\n' "$file" >&2
      exit 1
    fi
    if [[ ! -f "$skill_dir/$file" ]] || ! cmp -s "$source_file" "$skill_dir/$file"; then
      changed=true
    fi
  done

  revision="$(git -C "$temp_dir/arena" rev-parse HEAD)"
  if [[ "$changed" == false ]]; then
    printf 'Arena is current at %s\n' "$revision"
    exit 0
  fi

  mkdir -p "$skill_dir/scripts"
  for file in "${files[@]}"; do
    staged="$(mktemp "$skill_dir/$file.XXXXXX")"
    cp "$temp_dir/arena/$file" "$staged"
    chmod 644 "$staged"
    mv -f "$staged" "$skill_dir/$file"
  done
  printf 'Arena updated from GitHub to %s; reopen SKILL.md before continuing.\n' "$revision"
  if [[ "$ARENA_REEXEC" == "0" ]]; then
    ARENA_REEXEC=1 exec bash "$skill_dir/scripts/update.sh"
  fi
  exit 0
fi

remote_url="$(git -C "$skill_dir" remote get-url origin)"

case "$remote_url" in
  "https://github.com/$expected_repo"|"https://github.com/$expected_repo.git"|"git@github.com:$expected_repo.git") ;;
  *) printf 'Unexpected Arena origin: %s\n' "$remote_url" >&2; exit 1 ;;
esac

branch="$(git -C "$skill_dir" symbolic-ref --quiet --short HEAD)"
if [[ "$branch" != main ]]; then
  printf 'Arena update requires the main branch; found %s\n' "$branch" >&2
  exit 1
fi

if [[ -n "$(git -C "$skill_dir" status --porcelain)" ]]; then
  printf 'Arena update stopped: local skill files have changes.\n' >&2
  exit 1
fi

before="$(git -C "$skill_dir" rev-parse HEAD)"
GIT_TERMINAL_PROMPT=0 git -C "$skill_dir" pull --ff-only --no-rebase origin main
after="$(git -C "$skill_dir" rev-parse HEAD)"

if [[ "$before" == "$after" ]]; then
  printf 'Arena is current at %s\n' "$after"
else
  printf 'Arena updated from %s to %s; reopen SKILL.md before continuing.\n' "$before" "$after"
  if [[ "$ARENA_REEXEC" == "0" ]]; then
    ARENA_REEXEC=1 exec bash "$skill_dir/scripts/update.sh"
  fi
fi

