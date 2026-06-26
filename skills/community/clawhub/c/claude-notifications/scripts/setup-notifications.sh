#!/bin/bash
set -euo pipefail

# Claude Code Notification Setup
# Sets up native macOS notifications for local and devpod environments.
# Usage: ./setup-notifications.sh [--devpod <ssh-host>]

info()  { echo "✅ $*"; }
warn()  { echo "⚠️  $*"; }
error() { echo "❌ $*" >&2; exit 1; }

NOTIFY_PORT=19876
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
SCRIPTS_DIR="$CLAUDE_DIR/scripts"
LOGS_DIR="$CLAUDE_DIR/logs"
PLIST_PATH="$HOME/Library/LaunchAgents/com.claude.notify-listener.plist"
PYTHON3="$(command -v python3 || true)"
[[ -z "$PYTHON3" ]] && error "python3 is required but not found. Install via: brew install python3"

# ── Local Setup ──────────────────────────────────────────────────────────────

setup_local() {
    echo "── Setting up local notifications ──"

    mkdir -p "$SCRIPTS_DIR" "$LOGS_DIR"

    # Check terminal-notifier
    if ! command -v terminal-notifier >/dev/null 2>&1; then
        echo "Installing terminal-notifier..."
        brew install terminal-notifier || error "Failed to install terminal-notifier. Run: brew install terminal-notifier"
    fi
    info "terminal-notifier found at $(which terminal-notifier)"
    NOTIFIER_PATH="$(which terminal-notifier)"

    # Copy notify.sh
    cp "$SCRIPT_DIR/notify.sh" "$SCRIPTS_DIR/notify.sh"
    chmod +x "$SCRIPTS_DIR/notify.sh"
    info "Installed notify.sh"

    # Copy and configure notify-listener.py (replace placeholder with actual path)
    sed "s|__TERMINAL_NOTIFIER_PATH__|${NOTIFIER_PATH}|g" \
        "$SCRIPT_DIR/notify-listener.py" > "$SCRIPTS_DIR/notify-listener.py"
    chmod +x "$SCRIPTS_DIR/notify-listener.py"
    info "Installed notify-listener.py"

    # Create launchd plist
    cat > "$PLIST_PATH" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.notify-listener</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON3}</string>
        <string>${SCRIPTS_DIR}/notify-listener.py</string>
    </array>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
    <key>ProcessType</key>
    <string>Interactive</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
    <key>StandardOutPath</key>
    <string>${LOGS_DIR}/notify-listener.log</string>
    <key>StandardErrorPath</key>
    <string>${LOGS_DIR}/notify-listener.log</string>
</dict>
</plist>
PLIST
    info "Created launchd plist"

    # Stop existing listener if running
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
    # Kill any stale process on the port and wait for it to be free
    local stale_pids
    stale_pids="$(lsof -ti :${NOTIFY_PORT} 2>/dev/null || true)"
    [[ -n "$stale_pids" ]] && kill "$stale_pids" 2>/dev/null || true
    for _i in {1..10}; do
        lsof -ti :${NOTIFY_PORT} >/dev/null 2>&1 || break
        sleep 0.5
    done

    # Start listener
    launchctl load "$PLIST_PATH"
    sleep 1

    # Verify
    if lsof -i :${NOTIFY_PORT} >/dev/null 2>&1; then
        info "Notify listener running on port ${NOTIFY_PORT}"
    else
        warn "Listener may not have started. Check: cat $LOGS_DIR/notify-listener.log"
    fi

    # Configure Claude Code hooks in settings.json
    setup_hooks

    # Test
    echo ""
    echo "── Testing local notification ──"
    "$SCRIPTS_DIR/notify.sh" "Notifications setup complete!" "Claude Code" "Glass"
    info "Test notification sent. You should see a native macOS notification."
    echo ""
    echo "── Manual steps required ──"
    echo "1. Enable notifications for your terminal app:"
    echo "   System Settings > Notifications > [Warp / iTerm / Terminal]"
    echo "   → Set 'Allow Notifications' to ON, alert style to 'Banners' or 'Alerts'"
    echo ""
    echo "2. Enable notifications for Script Editor:"
    echo "   System Settings > Notifications > Script Editor"
    echo "   → Set 'Allow Notifications' to ON"
    echo "   (terminal-notifier routes through Script Editor)"
    echo ""
    echo "3. If using Focus/Do Not Disturb:"
    echo "   Add 'Script Editor' and your terminal app to Focus exceptions"
    echo "   OR turn off Do Not Disturb"
}

setup_hooks() {
    local settings="$CLAUDE_DIR/settings.json"
    if [ ! -f "$settings" ]; then
        echo '{}' > "$settings"
    fi

    # Validate settings.json is valid JSON
    if ! python3 -c "import json; json.load(open('$settings'))" 2>/dev/null; then
        warn "$settings is corrupt. Backing up and recreating."
        cp "$settings" "${settings}.bak"
        echo '{}' > "$settings"
    fi

    # Check if hooks already configured
    if python3 -c "
import json, sys
with open('$settings') as f:
    data = json.load(f)
if 'hooks' in data and 'Notification' in data.get('hooks', {}):
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
        info "Claude Code notification hooks already configured"
        return
    fi

    python3 -c "
import json
with open('$settings') as f:
    data = json.load(f)

data.setdefault('hooks', {})['Notification'] = [
    {
        'matcher': 'permission_prompt',
        'hooks': [{
            'type': 'command',
            'command': '~/.claude/scripts/notify.sh \"Claude Code needs your permission to proceed\" \"Claude Code - Action Required\" \"Ping\"',
            'timeout': 5
        }]
    },
    {
        'matcher': 'idle_prompt',
        'hooks': [{
            'type': 'command',
            'command': '~/.claude/scripts/notify.sh \"Claude has been waiting for your input (60+ seconds)\" \"Claude Code - Idle\" \"Glass\"',
            'timeout': 5
        }]
    },
    {
        'matcher': 'elicitation_dialog',
        'hooks': [{
            'type': 'command',
            'command': '~/.claude/scripts/notify.sh \"Additional input required for MCP tool\" \"Claude Code\" \"Submarine\"',
            'timeout': 5
        }]
    }
]

with open('$settings', 'w') as f:
    json.dump(data, f, indent=2)
"
    info "Configured Claude Code notification hooks"
}

setup_devpod_hooks() {
    local host="$1"
    ssh "$host" 'python3 -c "
import json, os

settings_path = os.path.expanduser(\"~/.claude/settings.json\")
os.makedirs(os.path.dirname(settings_path), exist_ok=True)

data = {}
if os.path.exists(settings_path):
    with open(settings_path) as f:
        data = json.load(f)

if \"hooks\" in data and \"Notification\" in data.get(\"hooks\", {}):
    print(\"hooks already configured\")
else:
    data.setdefault(\"hooks\", {})[\"Notification\"] = [
        {\"matcher\": \"permission_prompt\", \"hooks\": [{\"type\": \"command\", \"command\": \"~/.claude/scripts/notify.sh \\\"Claude Code needs your permission to proceed\\\" \\\"Claude Code - Action Required\\\" \\\"Ping\\\"\", \"timeout\": 5}]},
        {\"matcher\": \"idle_prompt\", \"hooks\": [{\"type\": \"command\", \"command\": \"~/.claude/scripts/notify.sh \\\"Claude has been waiting for your input (60+ seconds)\\\" \\\"Claude Code - Idle\\\" \\\"Glass\\\"\", \"timeout\": 5}]},
        {\"matcher\": \"elicitation_dialog\", \"hooks\": [{\"type\": \"command\", \"command\": \"~/.claude/scripts/notify.sh \\\"Additional input required for MCP tool\\\" \\\"Claude Code\\\" \\\"Submarine\\\"\", \"timeout\": 5}]}
    ]
    with open(settings_path, \"w\") as f:
        json.dump(data, f, indent=2)
    print(\"hooks configured\")
"'
    info "Configured Claude Code hooks on $host"
}

# ── Devpod Setup ─────────────────────────────────────────────────────────────

setup_devpod() {
    local host="$1"
    echo ""
    echo "── Setting up devpod: $host ──"

    # Verify SSH connectivity
    if ! ssh -o ConnectTimeout=10 "$host" "echo ok" >/dev/null 2>&1; then
        error "Cannot SSH to $host. Ensure the devpod is running."
    fi
    info "SSH connection to $host verified"

    # Create dirs and copy notify.sh
    ssh "$host" "mkdir -p ~/.claude/scripts"
    scp "$SCRIPTS_DIR/notify.sh" "$host:~/.claude/scripts/notify.sh"
    ssh "$host" "chmod +x ~/.claude/scripts/notify.sh"
    info "Installed notify.sh on $host"

    # Configure tmux passthrough
    ssh "$host" 'grep -q "allow-passthrough" ~/.tmux.conf 2>/dev/null && echo "already set" || (echo "" >> ~/.tmux.conf && echo "# Allow OSC escape sequences to pass through for notifications" >> ~/.tmux.conf && echo "set -g allow-passthrough on" >> ~/.tmux.conf && echo "added")'
    info "Configured tmux passthrough on $host"

    # Reload tmux config if tmux is running
    ssh "$host" 'tmux source-file ~/.tmux.conf 2>/dev/null || true'

    # Configure Claude Code hooks on devpod
    setup_devpod_hooks "$host"

    # Add RemoteForward to SSH config
    add_ssh_forward "$host"

    info "Devpod $host setup complete"
    echo "   ⮑ Start a NEW SSH session to $host for the reverse tunnel to activate."
}

add_ssh_forward() {
    local host="$1"
    local ssh_config="$HOME/.ssh/config"
    local forward_line="    RemoteForward ${NOTIFY_PORT} 127.0.0.1:${NOTIFY_PORT}"

    mkdir -p "$HOME/.ssh"
    touch "$ssh_config"
    chmod 600 "$ssh_config"

    # Check if RemoteForward already configured for this host using resolved SSH config
    if ssh -G "$host" 2>/dev/null | grep -qi "remoteforward.*${NOTIFY_PORT}"; then
        info "SSH RemoteForward already configured for $host"
        return
    fi

    # Use python3 with proper argument passing to safely modify SSH config
    python3 - "$ssh_config" "$host" "$forward_line" <<'PYEOF'
import re, sys

ssh_config = sys.argv[1]
host = sys.argv[2]
forward_line = sys.argv[3]

with open(ssh_config) as f:
    content = f.read()

lines = content.split('\n')
result = []
found_host = False
inserted = False
host_re = re.compile(r'^Host\s+.*\b' + re.escape(host) + r'\b')

for i, line in enumerate(lines):
    # If we found the host block and hit the next block or blank line, insert before it
    if found_host and not inserted:
        is_new_block = line.startswith('Host ')
        is_blank = not line.strip()
        if is_new_block or is_blank:
            result.append(forward_line)
            inserted = True
    result.append(line)
    if not found_host and host_re.match(line):
        found_host = True

# Host block was last in file, append at end
if found_host and not inserted:
    result.append(forward_line)

if not found_host:
    # Add new Host block
    result.append('')
    result.append(f'Host {host}')
    result.append(forward_line)

with open(ssh_config, 'w') as f:
    f.write('\n'.join(result))
PYEOF

    info "SSH RemoteForward configured for $host"
}

# ── Main ─────────────────────────────────────────────────────────────────────

usage() {
    echo "Usage: $0 [--devpod <ssh-host>] [--devpod <ssh-host>] ..."
    echo ""
    echo "Without --devpod: sets up local macOS notifications only."
    echo "With --devpod:    also configures specified devpod(s) for remote notifications."
    echo ""
    echo "Examples:"
    echo "  $0                                    # Local only"
    echo "  $0 --devpod myuser.devpod-ind         # Local + one devpod"
    echo "  $0 --devpod host1 --devpod host2      # Local + multiple devpods"
}

DEVPODS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --devpod)
            [[ -z "${2:-}" ]] && error "--devpod requires an SSH host argument"
            DEVPODS+=("$2")
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            error "Unknown argument: $1. Use --help for usage."
            ;;
    esac
done

# Always set up local first
setup_local

# Set up devpods if specified
for host in "${DEVPODS[@]}"; do
    setup_devpod "$host"
done

echo ""
echo "── Setup complete ──"
echo "Local notifications: ✅"
if [ ${#DEVPODS[@]} -gt 0 ]; then
    for host in "${DEVPODS[@]}"; do
        echo "Devpod $host:     ✅ (reconnect SSH for tunnel)"
    done
fi
