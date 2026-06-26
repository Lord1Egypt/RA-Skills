#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
collector="$script_dir/collect_changed_context.sh"
tmp_root="$(mktemp -d)"

cleanup() {
  rm -rf "$tmp_root"
}

trap cleanup EXIT

write_file() {
  local path="$1"
  local content="$2"

  mkdir -p "$(dirname "$path")"
  printf '%s\n' "$content" > "$path"
}

make_repo() {
  local name="$1"
  local repo="$tmp_root/$name"

  mkdir -p "$repo"
  git -C "$repo" init -q
  git -C "$repo" config user.name "Docs Refresh Test"
  git -C "$repo" config user.email "docs-refresh-test@example.com"
  git -C "$repo" commit --allow-empty -q -m "init"

  printf '%s\n' "$repo"
}

commit_all() {
  local repo="$1"
  local message="$2"

  git -C "$repo" add .
  git -C "$repo" commit -q -m "$message"
}

assert_line() {
  local output="$1"
  local expected="$2"

  if ! grep -Fxq "$expected" <<< "$output"; then
    echo "Expected line not found: $expected" >&2
    echo "--- collector output ---" >&2
    printf '%s\n' "$output" >&2
    exit 1
  fi
}

assert_routing() {
  local repo="$1"
  local expected_mode="$2"
  local expected_reason="$3"
  local output

  output="$(bash "$collector" "$repo")"
  assert_line "$output" "doc_system_mode=$expected_mode"
  assert_line "$output" "mode_reason=$expected_reason"
  assert_line "$output" "preferred_mode_doc=modes/$expected_mode.md"
}

repo="$(make_repo bootstrap)"
write_file "$repo/README.md" "# Overview"
commit_all "$repo" "bootstrap baseline"
assert_routing "$repo" "bootstrap" "no-doc-system"

repo="$(make_repo minimal)"
write_file "$repo/README.md" "# Overview"
write_file "$repo/AGENTS.md" "# AGENTS"
commit_all "$repo" "minimal baseline"
assert_routing "$repo" "minimal" "core-docs-without-split-domains"

repo="$(make_repo structured)"
write_file "$repo/AGENTS.md" "# AGENTS"
write_file "$repo/ARCHITECTURE.md" "# Architecture"
write_file "$repo/docs/design-docs/index.md" "# Design Docs"
commit_all "$repo" "structured baseline"
assert_routing "$repo" "structured" "split-doc-domains-present"

repo="$(make_repo repair)"
write_file "$repo/AGENTS.md" "# AGENTS"
mkdir -p "$repo/docs/design-docs"
commit_all "$repo" "repair baseline"
assert_routing "$repo" "repair" "missing-split-doc-indexes"

echo "Routing smoke tests passed."
