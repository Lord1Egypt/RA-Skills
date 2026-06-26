#!/bin/zsh
set -euo pipefail

export HOME="/Users/btai"
export PATH="/Users/btai/.bun/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
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

sleep 8

# NOTE: frpc is now a LaunchAgent (com.btai.frpc), NOT in tmux anymore

# core receivers
start_session "workout" "cd /Users/btai/butler-data && python3 workout_receiver.py"

# monitors
start_session "media-monitor" "cd /Users/btai/Projects/media-monitor/server && /Users/btai/Projects/media-monitor/venv/bin/python main.py"

# news dashboard
start_session "backend" "cd /Users/btai/Projects/news-dashboard/backend && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
start_session "news-frontend" "cd /Users/btai/Projects/news-dashboard/frontend && npm run dev -- --host 0.0.0.0 --port 5173"

# tempest
start_session "tempest-backend" "cd /Users/btai/Projects/tempest-os/apps/server && pnpm dev"
start_session "tempest-frontend" "cd /Users/btai/Projects/tempest-os/apps/dashboard && pnpm dev -- --host 0.0.0.0 --port 5188"

# paperclip
start_session "paperclip" "cd /Users/btai/.openclaw/workspace-lab/tmp/paperclip && PORT=3110 HOST=127.0.0.1 pnpm dev"

# obsidian sync
if command -v ob >/dev/null 2>&1; then
  start_session "obsidian-sync" "cd /Users/btai/Obsidian/BTAI && ob sync --continuous"
fi

log "bootstrap complete"
