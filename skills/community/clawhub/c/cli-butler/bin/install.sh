#!/usr/bin/env bash
# shellcheck disable=SC1091  # sibling lib files are sourced at runtime
# cli-butler F3: install — channel-routed install with plan + journal writeback.
# Flow: route channel (--channel override, else OS default) -> print plan ->
# execute unless --dry-run; an already-installed name is a no-op unless --yes.
set -u
case "$0" in */*) BIN_DIR=${0%/*} ;; *) BIN_DIR=. ;; esac
. "${BIN_DIR}/../lib/common.sh"
. "${BIN_DIR}/../lib/channels.sh"

DRY=0; YES=0; CH=""; name=""
while [ $# -gt 0 ]; do
  case "$1" in
    --channel) CH="${2:-}"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --yes) YES=1; shift ;;
    -h) usage; exit 0 ;;
    *) name="$1"; shift ;;
  esac
done
[ -n "$name" ] || die "usage: install <cli> [--channel id] [--dry-run] [--yes]"

# route: explicit --channel > OS default (darwin: brew; linux: apt > npm) >
# first available channel in CHANNELS order
if [ -z "$CH" ]; then
  if is_darwin && have brew; then CH=brew
  elif ! is_darwin && have apt; then CH=apt
  else
    for pair in $CHANNELS; do
      id=${pair%%:*}
      if channel_available "$id"; then CH=$id; break; fi
    done
  fi
fi
[ -n "$CH" ] || die "install: no available channel found"
channel_bin "$CH" >/dev/null 2>&1 || die "install: channel '$CH' not available on this machine"

cmd=$(channel_install_cmd "$CH" "$name") || die "install: cannot route '$name' via '$CH'"
echo "plan: channel=$CH"
echo "plan: $cmd"

# npm -g anti-hijack: warn when PATH npm and configured global prefix diverge
if [ "$CH" = "npm" ]; then
  pref=$(probe 5 npm prefix -g 2>/dev/null)
  npm_dir=$(cd -- "$(dirname -- "$(command -v npm)")" 2>/dev/null && pwd -P)
  [ -n "$pref" ] && [ -n "$npm_dir" ] && [ "$pref" != "$npm_dir" ] && \
    echo "prefix-warn: npm prefix -g ($pref) differs from PATH npm ($npm_dir)"
fi

# network constraint: reuse the machine's detected proxy when webget knows it
if have webget; then
  pu=$(webget --proxy-url 2>/dev/null)
  [ -n "$pu" ] && { export HTTPS_PROXY="$pu" HTTP_PROXY="$pu"; echo "proxy: using $pu"; }
else
  echo "proxy: set HTTPS_PROXY/HTTP_PROXY yourself if this machine needs one"
fi

if [ -n "$(journal_get "$name")" ] || channel_enumerate "$CH" 2>/dev/null | grep -qxF -- "$name"; then
  if [ "$YES" -eq 1 ]; then
    echo "note: '$name' already known; reinstalling (--yes)"
  else
    echo "note: '$name' already installed; nothing executed (dry-run by default)"
    echo "note: re-run with --yes to reinstall, or --dry-run to inspect the plan"
    exit 0
  fi
fi

if [ "$DRY" -eq 1 ]; then
  echo "dry-run: no changes made"
  exit 0
fi

if bash -c "$cmd"; then
  journal_add "$name" managed "$(date +%s)" "install:$CH" "$cmd"
  echo "ok: installed $name via $CH (journaled)"
else
  echo "install: command failed; nothing journaled" >&2
  exit 1
fi
