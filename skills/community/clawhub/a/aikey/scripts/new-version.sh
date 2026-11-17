#!/usr/bin/env bash
# Check whether the public AI KEY repo has newer skill versions than the ones installed here.
#
# Contract (the router relies on all of these):
#   - Prints ONE line only when at least one installed skill is older than the published one.
#   - Prints nothing in every other case: up to date, offline, timeout, unexpected format.
#   - Never exits non-zero, never prompts, never changes any skill file.
#   - Runs the network check at most once per 24 hours (stamp in ~/.aikey/last_version_check),
#     so offline hosts (bundle installs without network) pay the timeout at most once a day.
#
# Env overrides (for testing):
#   AIKEY_UPDATE_FORCE=1      ignore the 24h stamp
#   AIKEY_UPDATE_BASE=<url>   base URL that contains <skill>/SKILL.md (default: public repo main)
#   AIKEY_UPDATE_HOME=<dir>   where the stamp file lives (default: ~/.aikey)

set -u

PREFIX="${SKILL_PREFIX:-aikey}"
BASE="${AIKEY_UPDATE_BASE:-https://raw.githubusercontent.com/iamzifei/aikey/main/skills}"
STAMP_DIR="${AIKEY_UPDATE_HOME:-${HOME:-/tmp}/.aikey}"
STAMP="$STAMP_DIR/last_version_check"

# --- once per day -------------------------------------------------------------
now=$(date +%s)
if [ "${AIKEY_UPDATE_FORCE:-0}" != "1" ] && [ -f "$STAMP" ]; then
  last=$(cat "$STAMP" 2>/dev/null)
  case "$last" in ''|*[!0-9]*) last=0 ;; esac
  age=$((now - last))
  # A negative age means the clock went back; treat it as stale and check again.
  [ "$age" -ge 0 ] && [ "$age" -lt 86400 ] && exit 0
fi
# Write the stamp before the network call: a failed check must not retry on every run.
mkdir -p "$STAMP_DIR" 2>/dev/null && echo "$now" > "$STAMP" 2>/dev/null

command -v curl >/dev/null 2>&1 || exit 0

# --- local versions -------------------------------------------------------------
# Installed skills are the siblings of this router directory (scripts/ -> aikey/ -> skills root).
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." 2>/dev/null && pwd)" || exit 0

read_version() {  # first `version:` line inside the frontmatter
  awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f&&/^version:/{sub(/^version:[[:space:]]*/,"");print;exit}' "$1" 2>/dev/null
}

TMP="$(mktemp -d 2>/dev/null)" || exit 0
trap 'rm -rf "$TMP"' EXIT

for d in "$ROOT"/"$PREFIX"*/; do
  [ -f "$d/SKILL.md" ] || continue
  name=$(basename "${d%/}")
  v=$(read_version "$d/SKILL.md")
  [ -n "$v" ] && printf '%s %s\n' "$name" "$v" >> "$TMP/local"
done
[ -s "$TMP/local" ] || exit 0

# --- remote versions (parallel, 3s cap per request) -------------------------------
export BASE TMP
cut -d' ' -f1 "$TMP/local" | xargs -P 16 -I{} sh -c \
  'curl -fsL --max-time 3 "$BASE/$1/SKILL.md" -o "$TMP/$1.remote" 2>/dev/null || rm -f "$TMP/$1.remote"' _ {}

# --- compare -----------------------------------------------------------------------
newer=""
count=0
while read -r name lv; do
  f="$TMP/$name.remote"
  [ -s "$f" ] || continue
  rv=$(read_version "$f")
  case "$rv" in ''|*[!0-9.]*) continue ;; esac
  [ "$rv" = "$lv" ] && continue
  # newer only if the remote version sorts last
  top=$(printf '%s\n%s\n' "$lv" "$rv" | sort -t. -k1,1n -k2,2n -k3,3n | tail -1)
  [ "$top" = "$rv" ] || continue
  count=$((count + 1))
  [ "$count" -le 3 ] && newer="${newer}${newer:+、}${name} ${lv} → ${rv}"
done < "$TMP/local"

[ "$count" -eq 0 ] && exit 0
more=""
[ "$count" -gt 3 ] && more="（另有 $((count - 3)) 个）"
echo "AI KEY 有新版：${newer}${more}。更新方法：Claude Code / Codex 跑 \`npx skills add iamzifei/aikey -g --all\`；豆包 / WorkBuddy 把原来的下载地址再发一次。"
exit 0
