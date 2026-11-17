#!/usr/bin/env bash
# shellcheck disable=SC1091  # sibling lib files are sourced at runtime
# cli-butler F5: refchain — five-layer reference chain for one CLI.
# Layers: 1 realpath/chain  2 owner  3 PATH definition lines
#         4 launchd/cron    5 config-file references   + last-used.
set -u
case "$0" in */*) BIN_DIR=${0%/*} ;; *) BIN_DIR=. ;; esac
. "${BIN_DIR}/../lib/common.sh"
. "${BIN_DIR}/../lib/channels.sh"

name="${1:-}"
[ "${1:-}" = "-h" ] && { usage; exit 0; }
[ -n "$name" ] || die "usage: refchain <cli>"
command -v "$name" >/dev/null 2>&1 || die "refchain: '$name' not found on PATH"

p=$(command -v "$name")
echo "name=$name"
echo "path=$p"

# layer 1: symlink chain + realpath (relative hops normalized per hop)
chain="$p"; cur="$p"; hops=0
while [ -L "$cur" ] && [ "$hops" -lt 40 ]; do
  t=$(readlink -- "$cur") || break
  case "$t" in
    /*) cur="$t" ;;
    *) sub=${t%/*}; [ "$sub" = "$t" ] && sub=.  # plain name stays in same dir
       cur=$(cd -- "${cur%/*}/$sub" 2>/dev/null && pwd -P) || break
       cur="$cur/${t##*/}" ;;
  esac
  chain="$chain -> $cur"
  hops=$((hops + 1))
done
echo "chain=$chain"
rp=$(realpath_safe "$cur")
echo "realpath=$rp"

# layer 2: owner (channel|category) + owning package when derivable from layout
_resolve_owner_ret "$name" "$cur"
echo "owner=${OWNER:-unknown|unknown}"
case "$rp" in
  */Cellar/*) pkg=${rp#*/Cellar/}; pkg=${pkg%%/*}; echo "owned-by=$pkg (brew)" ;;
  */lib/node_modules/*) pkg=${rp#*/lib/node_modules/}; pkg=${pkg%/*}; pkg=${pkg#*/}; echo "owned-by=$pkg (npm)" ;;
esac

# word-boundary-safe grep helper: fixed-string line matches, file:line:text
grep_refs() { # <label> <pattern> <file...>
  local label="$1" pat="$2" f
  shift 2
  for f in "$@"; do
    [ -f "$f" ] || continue
    grep -nF -- "$pat" "$f" 2>/dev/null | while IFS= read -r hit; do
      printf '%s=%s\n' "$label" "$f:${hit%%:*}:${hit#*:}"
    done
  done
}

# layer 3: PATH definition lines — shell configs mentioning the dir or the name
pdir=${p%/*}  # cur drifts to the resolved target during the chain walk
IFS0=$IFS; IFS=:
# shellcheck disable=SC2086  # knob is a colon/space list on purpose
for f in ${BUTLER_SHELL_CONFIGS:-"$HOME/.zshrc" "$HOME/.zprofile" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile"}; do
  IFS=$IFS0
  grep_refs path-ref "$pdir" "$f"
  grep_refs path-ref "$name" "$f"
done
IFS=$IFS0

# layer 4: launchd plists (incl. disabled suffixes) + crontab
IFS0=$IFS; IFS=:
# shellcheck disable=SC2086  # knob is a colon/space list on purpose
for d in ${BUTLER_LAUNCHD_DIRS:-"$HOME/Library/LaunchAgents" /Library/LaunchAgents /Library/LaunchDaemons}; do
  IFS=$IFS0
  [ -d "$d" ] || continue
  for f in "$d"/*.plist "$d"/*.plist.*; do
    [ -f "$f" ] || continue
    if grep -qF -- "$name" "$f" 2>/dev/null || grep -qF -- "$rp" "$f" 2>/dev/null; then
      case "$f" in
        *.plist) echo "launchd-ref=$f" ;;
        *) echo "launchd-ref=$f (disabled)" ;;
      esac
    fi
  done
done
IFS=$IFS0
if have crontab; then
  crontab -l 2>/dev/null | grep -nF -- "$name" 2>/dev/null | while IFS= read -r hit; do
    printf 'cron-ref=crontab:%s:%s\n' "${hit%%:*}" "${hit#*:}"
  done
fi

# layer 5: well-known config files
IFS0=$IFS; IFS=:
# shellcheck disable=SC2086  # knob is a colon/space list on purpose
for f in ${BUTLER_CONFIG_FILES:-"$HOME/.ssh/config" "$HOME/.gitconfig" "$HOME/.curlrc" "$HOME/.wgetrc"}; do
  IFS=$IFS0
  grep_refs config-ref "$name" "$f"
  grep_refs config-ref "$rp" "$f"
done
IFS=$IFS0

# last-used: zsh extended history epoch (mtime is not trusted — bulk syncs)
lu=$(hist_last_used "$name")
if [ -n "$lu" ]; then
  echo "last-used=$lu ($(date -r "$lu" '+%Y-%m-%d %H:%M' 2>/dev/null))"
else
  echo "last-used=-"
fi
