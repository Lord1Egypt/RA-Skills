#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <mail-file>" >&2
  exit 1
fi

mail_file="$1"
[[ -f "$mail_file" ]] || { echo "Mail file not found" >&2; exit 1; }

source_dir="$(dirname "$mail_file")"
mail_root="$(dirname "$source_dir")"
keep_dir="$mail_root/keep"
mkdir -p "$keep_dir"

mv "$mail_file" "$keep_dir/"
printf '%s\n' "$keep_dir/$(basename "$mail_file")"
