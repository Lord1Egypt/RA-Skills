#!/bin/bash
# ttyd + tmux Web Terminal for Claude Code
# Persistent session with mouse support

set -e

PORT=${1:-6080}
WORKSPACE="${HOME}/workspace/claude-code"

# Create tmux config if not exists
mkdir -p ~/.config
cat > ~/.tmux.conf << 'EOF'
# UTF-8 support
set -g default-terminal "xterm-256color"
set -g utf8 on
set -g status-utf8 on

# Mouse support (scroll, click, resize)
set -g mouse on

# Better scrolling
set -g terminal-overrides 'xterm*:smcup@:rmcup@'
EOF

# Install tmux if needed
if ! command -v tmux &> /dev/null; then
    echo "Installing tmux..."
    apt-get update && apt-get install -y tmux
fi

# Kill existing ttyd
pkill -9 ttyd 2>/dev/null || true
sleep 1

# Start ttyd with tmux
echo "=== Starting ttyd + tmux ==="
nohup ttyd -p $PORT -W bash -c "export LANG=zh_CN.UTF-8; cd $WORKSPACE && tmux new -A -s main" > /tmp/ttyd.log 2>&1 &

sleep 2

# Verify
if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/ | grep -q "200"; then
    echo "✅ ttyd started on port $PORT"
else
    echo "❌ ttyd failed to start"
    exit 1
fi
