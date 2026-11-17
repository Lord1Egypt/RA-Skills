#!/usr/bin/env bash
# shellcheck disable=SC1091  # sibling lib files are sourced at runtime
# cli-butler F6: cap — capability enumeration from a CLI's own help output.
# Tries --help then -h then help; extracts usage line + top-level subcommands;
# unparseable output falls back to the raw first paragraph.
set -u
case "$0" in */*) BIN_DIR=${0%/*} ;; *) BIN_DIR=. ;; esac
. "${BIN_DIR}/../lib/common.sh"

name="${1:-}"
[ "${1:-}" = "-h" ] && { usage; exit 0; }
[ -n "$name" ] || die "usage: cap <cli>"
command -v "$name" >/dev/null 2>&1 || die "cap: '$name' not found on PATH"

help_text=""
for flag in --help -h help; do
  help_text=$(probe 10 "$name" "$flag" 2>/dev/null)
  # probe rc is masked by design; some tools print usage but exit non-zero, so
  # any non-empty output from a help flag counts
  [ -n "$help_text" ] && break
done
[ -n "$help_text" ] || die "cap: '$name' produced no help output"

echo "name=$name"

help_file="${TMPDIR:-/tmp}/butler-cap.$$"
printf '%s\n' "$help_text" > "$help_file"
trap 'rm -f "$help_file"' EXIT

usage_line=$(LC_ALL=C grep -iE '(^|[[:space:]])usage:' "$help_file" | head -1)
[ -n "$usage_line" ] && echo "usage=$usage_line"

# top-level subcommands: two-column rows under a Commands/… heading, or generic
# indented "word  description" rows outside Options blocks
cmds=$(LC_ALL=C awk '
  /^[[:space:]]*(commands|subcommands|available commands)[: ]*$/ { incmds=1; next }
  /^[[:space:]]*(options|flags|examples|description|aliases|arguments|global)/ { incmds=0 }
  incmds && $0 ~ /^ {2,}[^ ]/ {
    line=$0; sub(/^[[:space:]]+/, "", line)
    cmd=line; sub(/[[:space:]].*/, "", cmd)
    if (cmd !~ /^[-<>[\]{}|,]/ && cmd !~ /,|<|>|\[/) {
      desc=line; sub(/^[^[:space:]]+[[:space:]]*/, "", desc)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", desc)
      print "command=" cmd "\t" desc
    }
    next
  }
  !incmds && $0 ~ /^ {2,}[a-z][a-z0-9_-]*[[:space:]]{2,}/ {
    line=$0; sub(/^[[:space:]]+/, "", line)
    cmd=line; sub(/[[:space:]].*/, "", cmd)
    desc=line; sub(/^[^[:space:]]+[[:space:]]*/, "", desc)
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", desc)
    print "command=" cmd "\t" desc
  }
' "$help_file")

if [ -n "$cmds" ]; then
  printf '%s\n' "$cmds"
else
  # fallback: nothing parseable -> raw first paragraph (first non-blank block)
  raw=$(LC_ALL=C awk '/^[[:space:]]*$/ { if (seen) exit; next } { seen=1; print }' "$help_file" | head -5)
  [ -n "$raw" ] && printf 'raw=%s\n' "$raw"
fi
