#!/bin/zsh
# Runs inside a fresh iTerm2 pane: pane.zsh <tmux-session> <dir> <agent argv...>
# iTerm2 starts pane commands with a minimal PATH, so add the usual CLI locations.
emulate -LR zsh
path+=("$HOME/.local/bin" /opt/homebrew/bin /usr/local/bin)
session=$1 dir=$2
shift 2
# tmux runs the command only when it creates the session; otherwise -A attaches.
# A login shell gives the agent the same environment as a normal terminal.
exec tmux new-session -A -s "$session" -c "$dir" /bin/zsh -lic 'exec "$@"' zsh "$@"
