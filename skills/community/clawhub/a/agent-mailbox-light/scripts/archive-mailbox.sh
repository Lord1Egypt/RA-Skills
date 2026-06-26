#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <mail-file>" >&2
  exit 1
fi

mail_file="$1"
[[ -f "$mail_file" ]] || { echo "Mail file not found" >&2; exit 1; }

inbox_dir="$(dirname "$mail_file")"
mail_root="$(dirname "$inbox_dir")"
archive_dir="$mail_root/archive"
mkdir -p "$archive_dir"

mv "$mail_file" "$archive_dir/"
printf '%s\n' "$archive_dir/$(basename "$mail_file")"
