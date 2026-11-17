#!/usr/bin/env bash
# shellcheck disable=SC1091  # sibling lib files are sourced at runtime
# cli-butler list — grouped local CLI inventory (F1).
# Merges per-channel enumerations with a PATH scan; classifies each binary as
# managed / system / manual / untracked; collects one-line descriptions locally.
set -u
case "$0" in */*) BIN_DIR=${0%/*} ;; *) BIN_DIR=. ;; esac # no dirname fork; works with PATH=/nonexistent
. "${BIN_DIR}/../lib/common.sh"
. "${BIN_DIR}/../lib/channels.sh"
. "${BIN_DIR}/../lib/function.sh"

usage_list() {
  printf 'usage: cli-butler list [--kv] [--by-function] [--channel <id>]\n'
}

LIST_KV=0
LIST_CHANNEL=""
while [ $# -gt 0 ]; do
  case "$1" in
    --kv) LIST_KV=1 ;;
    --by-function) LIST_FUNC=1 ;;
    --channel) LIST_CHANNEL="${2:-}"; shift ;;
    -h|--help) usage_list; exit 0 ;;
    *) die 64 "list: unknown argument: $1" ;;
  esac
  shift
done
if [ -n "$LIST_CHANNEL" ]; then
  channel_bin "$LIST_CHANNEL" >/dev/null || die 64 "list: unknown channel: $LIST_CHANNEL"
fi

TAB=$'\t'
LF=$'\n'
ROWS="" # name\tversion\tchannel\tcategory\tpath\tsize\tdesc
SEEN="" # newline-separated names already emitted

seen_has() { case "$LF$SEEN$LF" in *"$LF$1$LF"*) return 0 ;; esac; return 1; } # zero-fork exact match
seen_add() { SEEN="$SEEN$1$LF"; }

humanize_size() { # bytes -> "1.2M" style; empty or "-" input -> "-" (pure bash: fork-free)
  case "$1" in ""|-) printf -- '-'; return ;; esac
  local b=$1 u r
  if [ "$b" -ge 1073741824 ]; then u=1073741824; r=G
  elif [ "$b" -ge 1048576 ]; then u=1048576; r=M
  elif [ "$b" -ge 1024 ]; then u=1024; r=K
  else printf '%dB' "$b"; return; fi
  printf '%d.%d%s' $((b / u)) $(( (b % u) * 10 / u )) "$r"
}

add_row() { # <name> <version> <channel> <category> <path>
  local n="$1" v="$2" ch="$3" cat="$4" p="$5" sz="" desc=""
  seen_has "$n" && return 0
  seen_add "$n"
  # channel_desc runs in a subshell (printf API); the whatis fallback must stay
  # in the main shell so the whatis budget/name cache survive across rows
  if [ "$cat" = "managed" ]; then desc=$(channel_desc "$ch" "$n"); fi
  if [ -z "$desc" ]; then whatis_desc "$n"; desc=$WHW_RET; fi
  sz="-"
  if [ "$p" != "-" ]; then sz=$(humanize_size "$(du_size "$p")"); fi
  ROWS="$ROWS$n${TAB}$v${TAB}$ch${TAB}$cat${TAB}$p${TAB}$sz${TAB}$desc$LF"
}

# 1) channel-managed entries (CHANNELS order = provenance priority);
#    enumeration warms the per-shell caches used by _resolve_owner_ret below
OWNED_INDEX="" # name\tchannel (rule3 fast path)
for pair in $CHANNELS; do
  id="${pair%%:*}"
  channel_enumerate "$id" >/dev/null 2>&1 || continue
done
# warm install-prefix caches in THIS shell so per-row desc lookups stay fork-free
for pair in $CHANNELS; do
  id="${pair%%:*}"
  channel_prefixes "$id" >/dev/null 2>&1 || true
  channel_desc_bulk "$id" >/dev/null 2>&1 || true
done
for pair in $CHANNELS; do
  id="${pair%%:*}"
  eval "enum=\"\${ENUM_$id:-}\""
  [ -n "$enum" ] || continue
  chunk=$(printf '%s\n' "$enum" | LC_ALL=C awk -F'\t' -v ch="$id" 'NF >= 2 { print $1"\t"ch }')
  OWNED_INDEX="$OWNED_INDEX$chunk$LF"
done

# journal name cache (rule4 fast path)
if [ -f "$JOURNAL" ]; then
  JNAMES_CACHE=$(awk -F'\t' 'NF >= 2 { print $1 }' "$JOURNAL")
else
  # shellcheck disable=SC2034  # consumed by _resolve_owner_ret via channels.sh
  JNAMES_CACHE=""
fi

for pair in $CHANNELS; do
  id="${pair%%:*}"
  channel_available "$id" || continue
  eval "enum=\"\${ENUM_$id:-}\""
  [ -n "$enum" ] || continue
  while IFS=$'\t' read -r n v; do
    [ -n "$n" ] || continue
    p=$(command -v "$n" 2>/dev/null)
    add_row "$n" "$v" "$id" managed "${p:--}"
  done <<EOF
$enum
EOF
done

# 2) PATH scan; first hit per basename wins (PATH semantics).
# BUTLER_LIST_PATH overrides the scanned path (tests narrow it for speed/determinism;
# command execution still uses full $PATH).
SCAN_PATH="${BUTLER_LIST_PATH:-$PATH}"
IFS0=$IFS
IFS=:
for d in $SCAN_PATH; do
  IFS=$IFS0
  [ -n "$d" ] || continue
  [ -d "$d" ] || continue
  for f in "$d"/*; do
    [ -e "$f" ] || continue
    [ -d "$f" ] && continue
    [ -x "$f" ] || continue
    n=${f##*/}
    seen_has "$n" && continue
    _resolve_owner_ret "$n" "$f" || true
    res=${OWNER:-manual|untracked}
    add_row "$n" "-" "${res%%|*}" "${res##*|}" "$f"
  done
done
IFS=$IFS0

rows_for() { # optional channel filter; prints ROWS
  while IFS=$'\t' read -r n v ch cat p sz desc; do
    [ -n "$n" ] || continue
    [ -z "$LIST_CHANNEL" ] || [ "$ch" = "$LIST_CHANNEL" ] || continue
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$n" "$v" "$ch" "$cat" "$p" "$sz" "$desc"
  done <<EOF
$ROWS
EOF
}

if [ "$LIST_KV" -eq 1 ]; then
  rows_for | while IFS=$'\t' read -r n v ch cat p sz desc; do
    [ -n "$n" ] || continue
    kv_field name "$n"; kv_field version "$v"; kv_field channel "$ch"; kv_field category "$cat"
    kv_field path "$p"; kv_field size "$sz"; kv_field desc "$desc"
    echo
  done
  exit 0
fi

group_blurb() {
  case "$1" in
    brew) printf 'Homebrew-managed tools' ;;
    npm) printf 'global npm packages' ;;
    pnpm) printf 'global pnpm packages' ;;
    pipx) printf 'pipx-installed Python CLIs' ;;
    uv) printf 'uv tool-installed Python CLIs' ;;
    cargo) printf 'cargo-installed Rust binaries' ;;
    gem) printf 'Ruby gems providing executables' ;;
    apt) printf 'Debian/Ubuntu packages' ;;
    system) printf 'system-bundled (SIP-protected, NOT uninstallable)' ;;
    manual) printf 'manually installed (journaled)' ;;
    untracked) printf 'unowned binaries on PATH' ;;
  esac
}

FILTERED=$(rows_for)

if [ "${LIST_FUNC:-0}" -eq 1 ]; then
  # function view: purpose groups, channel shown as a per-row attribute
  FUNC_BUCKETS=""
  FUNC_TEXT=""
  while IFS=$'\t' read -r n v ch cat p sz desc; do
    [ -n "$n" ] || continue
    categorize "$cat" "$n" "$desc"
    fc=$FUNC_CAT
    case "$LF$FUNC_BUCKETS" in *"|$fc|"*) ;; *) FUNC_BUCKETS="$FUNC_BUCKETS|$fc|";; esac
    FUNC_TEXT="$FUNC_TEXT$fc${TAB}$n${TAB}$v${TAB}$ch${TAB}$sz${TAB}$desc$LF"
  done <<EOF
$FILTERED
EOF
  FUNC_ORDER="AI / Agent 工具
移动开发
容器 / 基础设施
版本控制
库依赖
Web / 网络
多媒体
语言运行时
系统自带（SIP）
其他独立工具"
  while IFS='|' read -r g; do
    [ -n "$g" ] || continue
    case "$FUNC_BUCKETS" in *"|$g|"*) ;; *) continue;; esac
    gcount=0; gtext=""
    while IFS=$'\t' read -r fc n v ch sz desc; do
      [ "$fc" = "$g" ] || continue
      gcount=$((gcount + 1))
      gtext="$gtext$n${TAB}$v${TAB}$ch${TAB}$sz${TAB}$desc$LF"
    done <<EOF
$FUNC_TEXT
EOF
    [ "$gcount" -gt 0 ] || continue
    case "$g" in
      "系统自带（SIP）") blurb="system-bundled (SIP-protected, NOT uninstallable)" ;;
      "库依赖") blurb="libraries pulled in by the tools above" ;;
      "其他独立工具") blurb="standalone tools outside the named categories" ;;
      *) blurb="" ;;
    esac
    printf '== %s (%d)' "$g" "$gcount"
    [ -n "$blurb" ] && printf ' - %s' "$blurb"
    printf ' ==
'
    w1=4; w2=7; w3=6
    while IFS=$'\t' read -r n v ch sz desc; do
      [ -n "$n" ] || continue
      [ "${#n}" -gt "$w1" ] && w1=${#n}
      [ "${#v}" -gt "$w2" ] && w2=${#v}
      [ "${#ch}" -gt "$w3" ] && w3=${#ch}
    done <<EOF
$gtext
EOF
    printf '%-*s  %-*s  %-*s  %-6s  %s
' "$w1" NAME "$w2" VERSION "$w3" CH SIZE DESC
    while IFS=$'\t' read -r n v ch sz desc; do
      [ -n "$n" ] || continue
      printf '%-*s  %-*s  %-*s  %-6s  %s
' "$w1" "$n" "$w2" "$v" "$w3" "$ch" "$sz" "$desc"
    done <<EOF
$gtext
EOF
    echo ""
  done <<EOF
$FUNC_ORDER
EOF
  exit 0
fi

for g in brew npm pnpm pipx uv cargo gem apt system manual untracked; do
  gcount=0
  gtext=""
  while IFS=$'\t' read -r n v ch cat p sz desc; do
    [ -n "$n" ] || continue
    key=$ch; [ "$cat" = "managed" ] || key=$cat
    [ "$key" = "$g" ] || continue
    gcount=$((gcount + 1))
    gtext="$gtext$n${TAB}$v${TAB}$sz${TAB}$desc$LF"
  done <<EOF
$FILTERED
EOF
  [ "$gcount" -gt 0 ] || continue
  printf '== %s (%d) - %s ==\n' "$g" "$gcount" "$(group_blurb "$g")"
  w1=4; w2=7
  while IFS=$'\t' read -r n v sz desc; do
    [ -n "$n" ] || continue
    [ "${#n}" -gt "$w1" ] && w1=${#n}
    [ "${#v}" -gt "$w2" ] && w2=${#v}
  done <<EOF
$gtext
EOF
  printf '%-*s  %-*s  %-6s  %s\n' "$w1" NAME "$w2" VERSION SIZE DESC
  while IFS=$'\t' read -r n v sz desc; do
    [ -n "$n" ] || continue
    printf '%-*s  %-*s  %-6s  %s\n' "$w1" "$n" "$w2" "$v" "$sz" "$desc"
  done <<EOF
$gtext
EOF
  echo ""
done
exit 0
