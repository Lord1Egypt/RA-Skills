#!/usr/bin/env bash
# shellcheck disable=SC1091  # sibling lib files are sourced at runtime
# cli-butler F4: uninstall — system refusal, channel routing, dry-run-by-default
# for manual/untracked, launchd plist moved (not bootout-only), journal writeback.
# Red lines (REQUIREMENTS.md): system items are never uninstalled; channel-owned
# paths are removed via their channel, never `rm`'d; app-internal symlinks are
# only moved to .bak, never deleted.
set -u
case "$0" in */*) BIN_DIR=${0%/*} ;; *) BIN_DIR=. ;; esac
. "${BIN_DIR}/../lib/common.sh"
. "${BIN_DIR}/../lib/channels.sh"

usage() {
  cat <<'EOF'
cli-butler uninstall — remove a CLI safely (default: dry-run plan, no changes)

usage: uninstall <cli> [--yes]
       uninstall -h

safety matrix:
  system item          refused outright (SIP / system integrity) — no plan, no action
  channel item         plan via owning channel; --yes runs the channel's uninstall
  manual (journaled)   refchain summary + dry-run; --yes removes file, clears journal,
                       moves referencing launchd plists to *.plist.off
  untracked            same gate as manual (refchain shown first)
EOF
}

YES=0; name=""
while [ $# -gt 0 ]; do
  case "$1" in
    --yes) YES=1; shift ;;
    -h) usage; exit 0 ;;
    *) name="$1"; shift ;;
  esac
done
[ -n "$name" ] || { usage >&2; exit 64; }

path=$(command -v -- "$name" 2>/dev/null)
[ -n "$path" ] || die "uninstall: '$name' not found on PATH"

# 1) system items: refuse outright (red line)
_resolve_owner_ret "$name" "$path"
cat=${OWNER##*|}
ch=${OWNER%%|*}
if [ "$cat" = "system" ]; then
  echo "uninstall: '$name' ($path) is a system binary — refusing." >&2
  echo "uninstall: system tools are protected by SIP / system integrity and cannot be removed." >&2
  exit 1
fi

# 2) channel-managed: route through the owning channel, never rm
if [ "$cat" = "managed" ] && [ "$ch" != "manual" ]; then
  cmd=$(channel_uninstall_cmd "$ch" "$name") || die "uninstall: cannot route '$name' via '$ch'"
  echo "plan: channel=$ch"
  echo "plan: $cmd"
  if [ "$YES" -ne 1 ]; then
    echo "note: dry-run by default; re-run with --yes to execute via $ch"
    exit 0
  fi
  if bash -c "$cmd"; then
    [ -n "$(journal_get "$name")" ] && journal_del "$name"
    echo "ok: '$name' removed via $ch"
  else
    echo "uninstall: channel command failed; nothing changed" >&2
    exit 1
  fi
  exit 0
fi

# 3) manual / untracked: refchain summary + dry-run gate
echo "refs: checking references for '$name' ($path) before removal"
"$BIN_DIR/refchain.sh" "$name" 2>/dev/null | sed 's/^/refs:   /'
echo "plan: rm $path"
# launchd plists referencing this binary are moved aside (dsh lesson: bootout
# alone only ends the current session; the plist must be moved to stay disabled)
PLIST_HIT=$(find "$HOME/Library/LaunchAgents" /Library/LaunchAgents -maxdepth 1 \
  -name '*.plist' -type f 2>/dev/null | while IFS= read -r pl; do
    grep -lF -- "$path" "$pl" 2>/dev/null || grep -lF -- "$name" "$pl" 2>/dev/null
  done | head -5)
[ -n "$PLIST_HIT" ] && printf 'plan: mv %s <same>.off\n' "$PLIST_HIT"
if [ "$YES" -ne 1 ]; then
  echo "note: dry-run by default — nothing executed; re-run with --yes to remove"
  exit 0
fi
for pl in $PLIST_HIT; do
  mv -f "$pl" "$pl.off" && echo "ok: moved $pl -> $pl.off"
done
rm -f -- "$path" && echo "ok: removed $path"
[ -n "$(journal_get "$name")" ] && journal_del "$name"
echo "ok: '$name' uninstalled (manual path)"
