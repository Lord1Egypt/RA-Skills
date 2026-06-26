#!/usr/bin/env bash
set -euo pipefail

VERSION="3.0.0"
SCRIPT_NAME="bingo"
DATA_DIR="$HOME/.local/share/bingo"
mkdir -p "$DATA_DIR"

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com

_info()  { echo "[INFO]  $*"; }
_error() { echo "[ERROR] $*" >&2; }
die()    { _error "$@"; exit 1; }

cmd_card() {
    echo '  B   I   N   G   O'; for col in 1 2 3 4 5; do printf '%3d %3d %3d %3d %3d
' $(shuf -i $((col*15-14))-$((col*15)) -n 5); done
}

cmd_call() {
    echo "Called: $(shuf -i 1-75 -n 1)"
}

cmd_new_game() {
    : > $DATA_DIR/calls.txt && echo 'New game started'
}

cmd_history() {
    cat $DATA_DIR/calls.txt 2>/dev/null || echo 'No calls yet'
}

cmd_check() {
    local numbers="${2:-}"
    [ -z "$numbers" ] && die "Usage: $SCRIPT_NAME check <numbers>"
    echo 'Checking: $2'
}

cmd_stats() {
    echo 'Calls: '$(wc -l < $DATA_DIR/calls.txt 2>/dev/null || echo 0)
}

cmd_help() {
    echo "$SCRIPT_NAME v$VERSION"
    echo ""
    echo "Commands:"
    printf "  %-25s\n" "card"
    printf "  %-25s\n" "call"
    printf "  %-25s\n" "new-game"
    printf "  %-25s\n" "history"
    printf "  %-25s\n" "check <numbers>"
    printf "  %-25s\n" "stats"
    printf "  %%-25s\n" "help"
    echo ""
    echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
}

cmd_version() { echo "$SCRIPT_NAME v$VERSION"; }

main() {
    local cmd="${1:-help}"
    case "$cmd" in
        card) shift; cmd_card "$@" ;;
        call) shift; cmd_call "$@" ;;
        new-game) shift; cmd_new_game "$@" ;;
        history) shift; cmd_history "$@" ;;
        check) shift; cmd_check "$@" ;;
        stats) shift; cmd_stats "$@" ;;
        help) cmd_help ;;
        version) cmd_version ;;
        *) die "Unknown: $cmd" ;;
    esac
}

main "$@"
