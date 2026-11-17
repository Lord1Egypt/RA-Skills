#!/usr/bin/env bash
# shellcheck disable=SC1091  # sibling lib files are sourced at runtime
# cli-butler F2: manage — per-CLI info, channel-native outdated, upgrade routing.
# Channels without a native "what's latest" command are reported as unsupported
# (no guessing), per REQUIREMENTS.md.
set -u
case "$0" in */*) BIN_DIR=${0%/*} ;; *) BIN_DIR=. ;; esac
. "${BIN_DIR}/../lib/common.sh"
. "${BIN_DIR}/../lib/channels.sh"

usage() {
  cat <<'EOF'
cli-butler manage — per-CLI info, outdated, upgrade

usage: manage info <cli>            path / symlink chain / owner / size / refs
       manage outdated [--channel id]
       manage upgrade <cli> [--yes] dry-run by default
       manage -h
EOF
}

sub="${1:-}"
shift 2>/dev/null || true

case "$sub" in
  -h) usage; exit 0 ;;
  info)
    name="${1:-}"
    [ -n "$name" ] || { usage >&2; exit 64; }
    command -v "$name" >/dev/null 2>&1 || die "manage: '$name' not found on PATH"
    "$BIN_DIR/refchain.sh" "$name"
    rp=$(realpath_safe "$(command -v -- "$name")")
    echo "size=$(du_size "$rp")"
    ;;
  outdated)
    CH=""
    while [ $# -gt 0 ]; do
      case "$1" in
        --channel) CH="${2:-}"; shift 2 ;;
        *) shift ;;
      esac
    done
    channels_outdated() { # <id> -> prints "<name> <installed> -> <latest>" lines
      case "$1" in
        brew)
          probe 120 brew outdated --versions 2>/dev/null | \
            awk '{ n=$1; sub(/^\(/,"",$2); printf "%s %s -> %s\n", n, $2, $NF }'
          ;;
        npm)
          probe 120 npm outdated -g --depth=0 2>/dev/null | \
            awk 'NR>1 && NF>=4 && $3 != $4 { printf "%s %s -> %s\n", $1, $3, $4 }'
          ;;
        *) return 1 ;;
      esac
    }
    if [ -n "$CH" ]; then
      if channels_outdated "$CH"; then :; else
        echo "outdated: channel '$CH' has no native outdated command in cli-butler v0.1 — not supported, not guessing" >&2
        exit 1
      fi
      exit 0
    fi
    for pair in $CHANNELS; do
      id=${pair%%:*}
      channel_available "$id" || continue
      echo "== $id"
      if channels_outdated "$id"; then :; else
        echo "   not supported by cli-butler v0.1 (no native outdated)"
      fi
    done
    ;;
  upgrade)
    YES=0; name=""
    while [ $# -gt 0 ]; do
      case "$1" in
        --yes) YES=1; shift ;;
        *) name="$1"; shift ;;
      esac
    done
    [ -n "$name" ] || { usage >&2; exit 64; }
    path=$(command -v -- "$name" 2>/dev/null) || die "manage: '$name' not found on PATH"
    _resolve_owner_ret "$name" "$path"
    cat=${OWNER##*|}; ch=${OWNER%%|*}
    [ "$cat" = "managed" ] || die "manage: '$name' is $cat — upgrade only applies to channel-managed CLIs"
    cmd=$(channel_upgrade_cmd "$ch" "$name") || die "manage: cannot route upgrade for '$name' via '$ch'"
    echo "plan: channel=$ch"
    echo "plan: $cmd"
    if [ "$YES" -ne 1 ]; then
      echo "note: dry-run by default; re-run with --yes to execute"
      exit 0
    fi
    if bash -c "$cmd"; then
      echo "ok: '$name' upgraded via $ch"
    else
      echo "manage: upgrade failed; nothing changed" >&2
      exit 1
    fi
    ;;
  *) usage >&2; exit 64 ;;
esac
