# Bootstrap Script 模板

```bash
#!/bin/zsh
set -euo pipefail

export HOME="{{HOME}}"
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
SOCKET_DIR="/tmp/openclaw-tmux"
SOCKET="$SOCKET_DIR/openclaw.sock"
mkdir -p "$SOCKET_DIR"

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

ensure_tmux() {
  if ! tmux -S "$SOCKET" list-sessions >/dev/null 2>&1; then
    rm -f "$SOCKET"
    tmux -S "$SOCKET" start-server
  fi
}

start_session() {
  local session="$1"
  local cmd="$2"
  ensure_tmux
  if tmux -S "$SOCKET" has-session -t "$session" 2>/dev/null; then
    log "skip $session (already running)"
    return
  fi
  tmux -S "$SOCKET" new-session -d -s "$session" "$cmd"
  log "started $session"
}

sleep {{BOOT_DELAY}}

{{#SERVICES}}
start_session "{{SESSION}}" "cd {{WORKDIR}} && {{COMMAND}}"
{{/SERVICES}}

log "bootstrap complete"
```

## 重點
- `sleep` 等網路起來，建議 8-15 秒
- `start_session` 有 skip 邏輯，不會覆蓋已存在的 session
- 所有 session 用 OpenClaw socket
