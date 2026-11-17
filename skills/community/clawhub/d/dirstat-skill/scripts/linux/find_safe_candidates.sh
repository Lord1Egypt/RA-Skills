#!/usr/bin/env bash
set -euo pipefail

print_section() {
  local title="$1"
  shift
  echo "=== ${title} ==="
  "$@"
  echo
}

find_large_files() {
  local root="$1"
  if [ ! -d "$root" ]; then
    return 0
  fi
  find "$root" -type f -size +1G -printf '%s\t%p\n' | sort -rn
}

find_partial_files() {
  find "$HOME" -type f \( -name '*.filepart' -o -name '*.part' -o -name '*.partial' \) -printf '%s\t%p\n' | sort -rn
}

print_section "Large cache files >1G" find_large_files "$HOME/.cache"
print_section "Partial download files" find_partial_files
print_section "Trash files >1G" find_large_files "$HOME/.local/share/Trash"
print_section "Dot-trash files >1G" find_large_files "$HOME/.Trash"
