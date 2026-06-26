#!/bin/bash
set -euo pipefail

# Claude Code notification script.
# On macOS: uses terminal-notifier for native notifications.
# On devpod/remote: sends via SSH reverse tunnel to local listener,
# falls back to OSC 9 escape sequence.

debug() {
    [[ "${DEBUG:-}" == "1" ]] && echo "[DEBUG] $*" >&2 || true
}

if [ $# -lt 1 ]; then
    echo "Usage: $0 <message> [title] [sound]" >&2
    exit 1
fi

MESSAGE="$1"
TITLE="${2:-Claude Code}"
SOUND="${3:-Glass}"

debug "Message: $MESSAGE"
debug "Title: $TITLE"
debug "Sound: $SOUND"

# Remote: send via SSH reverse tunnel to local notify-listener
NOTIFY_PORT=19876
send_remote() {
    local payload
    payload=$(python3 -c "import json,sys;print(json.dumps({'message':sys.argv[1],'title':sys.argv[2],'sound':sys.argv[3]}))" "$MESSAGE" "$TITLE" "$SOUND")
    debug "Sending via reverse tunnel on port $NOTIFY_PORT"
    if curl -s -m 3 -X POST "http://127.0.0.1:${NOTIFY_PORT}" \
        -H "Content-Type: application/json" \
        -d "$payload" >/dev/null 2>&1; then
        debug "Notification sent via tunnel"
        return 0
    else
        debug "Tunnel not available, falling back to OSC 9"
        return 1
    fi
}

# OSC 9 fallback (in-app notification in some terminals)
send_osc9() {
    local msg="$1"
    if [[ -n "${TMUX:-}" ]]; then
        debug "Inside tmux, using DCS passthrough for OSC 9"
        printf '\ePtmux;\e\e]9;%s\a\e\\' "$msg"
    else
        debug "Sending OSC 9 directly"
        printf '\e]9;%s\a' "$msg"
    fi
}

# If terminal-notifier is not available (devpod/remote), use reverse tunnel
if ! command -v terminal-notifier >/dev/null 2>&1; then
    debug "terminal-notifier not found, trying reverse tunnel"
    send_remote || send_osc9 "$TITLE: $MESSAGE"
    exit 0
fi

# Local macOS: detect terminal for click-to-activate
BUNDLE_ID=""
case "${TERM_PROGRAM:-}" in
    "WarpTerminal")  BUNDLE_ID="dev.warp.Warp-Stable" ;;
    "iTerm.app")     BUNDLE_ID="com.googlecode.iterm2" ;;
    "Apple_Terminal") BUNDLE_ID="com.apple.Terminal" ;;
    "vscode")        BUNDLE_ID="com.microsoft.VSCode" ;;
    "Hyper")         BUNDLE_ID="co.zeit.hyper" ;;
    "Alacritty")     BUNDLE_ID="org.alacritty" ;;
    "kitty")         BUNDLE_ID="net.kovidgoyal.kitty" ;;
esac

if [[ -n "$BUNDLE_ID" ]]; then
    terminal-notifier -message "$MESSAGE" -title "$TITLE" -sound "$SOUND" -activate "$BUNDLE_ID"
else
    terminal-notifier -message "$MESSAGE" -title "$TITLE" -sound "$SOUND"
fi
