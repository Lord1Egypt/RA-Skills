#!/bin/bash
#
# ClawShorts - Multi-Device Shorts Limiter
# Delegates device management to Python CLI
#

set -euo pipefail

# Resolve symlinks to get the real script location
_real_script() {
    local src="$1"
    while [[ -L "$src" ]]; do
        src="$(readlink "$src")"
    done
    dirname "$src"
}
SCRIPT_DIR="$(_real_script "$0")"
CLAWSHORTS_PY="${SCRIPT_DIR}/../src/clawshorts/cli.py"
LOG_FILE="${HOME}/.clawshorts.log"

# Default config
DEFAULT_LIMIT=300

# ============ PYTHON CLI ============
run_python_cli() {
    local cmd="$1"
    shift
    PYTHONPATH="${SCRIPT_DIR}/../src" python3 "$CLAWSHORTS_PY" "$cmd" "$@"
}

# ============ COMMANDS THAT USE PYTHON ============
cmd_setup() {
    run_python_cli setup "$@"
}

cmd_add() {
    run_python_cli add "$@"
}

cmd_remove() {
    run_python_cli remove "$@"
}

cmd_list() {
    run_python_cli list "$@"
}

cmd_status() {
    run_python_cli status "$@"
}

cmd_reset() {
    # Delegate to Python CLI — uses SQLite only (no text file state)
    run_python_cli reset "${1:-}"
}

cmd_enable() {
    run_python_cli enable "$@"
}

cmd_disable() {
    run_python_cli disable "$@"
}

cmd_logs() {
    local lines="${1:-50}"
    local log_path="${HOME}/.clawshorts/daemon.log"
    if [[ ! -f "$log_path" ]]; then
        echo "No daemon.log found."
        return 1
    fi
    tail -n "$lines" "$log_path"
}

# ============ COMMANDS THAT USE ADB (KEEP IN BASH) ============
check_adb() {
    command -v adb &> /dev/null
}

install_adb() {
    echo "Installing ADB..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update -qq && sudo apt-get install -y adb
    elif command -v brew &> /dev/null; then
        brew install android-platform-tools
    else
        echo "ERROR: No supported package manager found (apt-get or brew)."
        echo "  Install ADB manually: https://developer.android.com/tools/adb"
        return 1
    fi
    echo "ADB installed successfully"
}

# Delegated to Python CLI (kept for reference, Python cmd_connect now handles this)
cmd_connect_py() {
    run_python_cli connect "$@"
}

cmd_start() {
    echo "Starting ClawShorts daemon..."
    echo "Daemon reads device config from SQLite automatically."
    PYTHONPATH="$SCRIPT_DIR/../src" exec python3 "$SCRIPT_DIR/clawshorts-daemon.py"
}

cmd_stop() {
    local pids
    pids=$(pgrep -f "clawshorts-daemon" 2>/dev/null || true)
    if [[ -z "$pids" ]]; then
        echo "Daemon not running"
        return 0
    fi
    # Graceful shutdown: SIGTERM first, wait 2s, then SIGKILL
    kill -TERM $pids 2>/dev/null || true
    sleep 2
    pkill -f "clawshorts-daemon" 2>/dev/null || true
    echo "✅ Stopped"
}

cmd_install() {
    # Create bin symlink so `shorts` works from anywhere
    local bin_dir="/opt/homebrew/bin"
    local symlink="${bin_dir}/shorts"
    if [[ ! -L "$symlink" ]] && [[ ! -e "$symlink" ]]; then
        if ln -s "$SCRIPT_DIR/clawshorts.sh" "$symlink" 2>/dev/null; then
            echo "✅ Linked: shorts → $symlink"
        else
            echo "⚠️  Could not create $symlink (need sudo?) — add $SCRIPT_DIR to your PATH instead"
        fi
    fi

    if [[ "$(uname)" == "Darwin" ]]; then
        _install_launchd
    else
        _install_systemd
    fi

    # Verify installation
    echo ""
    echo "Running verification..."
    sleep 3
    cmd_status
}

_install_launchd() {
    local plist="${HOME}/Library/LaunchAgents/com.fink.clawshorts.plist"
    mkdir -p "$(dirname "$plist")"
    
    cat > "$plist" << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.fink.clawshorts</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>${SCRIPT_DIR}/clawshorts-daemon.py</string>
        <string>--debug</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${LOG_FILE}</string>
    <key>StandardErrorPath</key>
    <string>${LOG_FILE}</string>
</dict>
</plist>
PLISTEOF
    
    # Unload existing first, then load fresh
    launchctl unload "$plist" 2>/dev/null || true
    launchctl load "$plist" 2>/dev/null || true
    
    echo "✅ Installed auto-start (launchd)"
    echo "   Daemon reads devices from SQLite automatically."
}

_install_systemd() {
    local unit_dir="${HOME}/.config/systemd/user"
    local unit_file="${unit_dir}/clawshorts.service"
    mkdir -p "$unit_dir"
    
    cat > "$unit_file" << UNITEOF
[Unit]
Description=ClawShorts YouTube Shorts Limiter
After=network.target

[Service]
Type=simple
ExecStart=$(command -v python3) ${SCRIPT_DIR}/clawshorts-daemon.py
Restart=on-failure
RestartSec=10
StandardOutput=append:${LOG_FILE}
StandardError=append:${LOG_FILE}

[Install]
WantedBy=default.target
UNITEOF
    
    systemctl --user daemon-reload
    systemctl --user enable --now clawshorts.service
    echo "✅ Installed auto-start (systemd)"
}

cmd_uninstall() {
    if [[ "$(uname)" == "Darwin" ]]; then
        local plist="${HOME}/Library/LaunchAgents/com.fink.clawshorts.plist"
        launchctl unload "$plist" 2>/dev/null || true
        rm -f "$plist"
    else
        systemctl --user disable --now clawshorts.service 2>/dev/null || true
        rm -f "${HOME}/.config/systemd/user/clawshorts.service"
        systemctl --user daemon-reload 2>/dev/null || true
    fi
    cmd_stop
    echo "✅ Uninstalled"
}

# ============ MAIN ============
# Parse command and arguments
_real_cmd="${1:-status}"

if [[ "$_real_cmd" == "shorts" ]]; then
    _verb="${2:-status}"
    if [[ $# -ge 3 ]]; then
        set -- "$_verb" "${@:3}"
    else
        set -- "$_verb"
    fi
    _cmd="$_verb"
else
    _cmd="$_real_cmd"
fi

case "$_cmd" in
    setup)    cmd_setup "${2:-}" "${3:-}" ;;
    add)      cmd_add "${2:-}" "${3:-}" ;;
    remove)   cmd_remove "${2:-}" ;;
    list)     cmd_list ;;
    status)   cmd_status "${2:-}" ;;
    reset)    cmd_reset "${2:-}" ;;
    enable)   cmd_enable "${2:-}" ;;
    disable)  cmd_disable "${2:-}" ;;
    connect)  cmd_connect "${2:-}" ;;
    start)    cmd_start "${2:-}" "${3:-}" ;;
    stop)     cmd_stop ;;
    install)  cmd_install "${2:-}" "${3:-}" ;;
    uninstall) cmd_uninstall ;;
    history)  run_python_cli history ${@:2} ;;
    logs)
        cmd_logs
        ;;
    *)
        echo "⚡ ClawShorts - YouTube Shorts Blocker"
        echo ""
        echo "Usage: shorts <command> [options]"
        echo ""
        echo "Commands:"
        echo "  shorts status        Show quota status"
        echo "  shorts reset        Reset today's quota"
        echo "  shorts stop         Stop the limiter"
        echo "  shorts start        Start the limiter"
        echo "  shorts install      Auto-start at login"
        echo "  shorts history      Show watch history (last 30 days)"
        echo "  shorts logs         Show debug logs"
        echo "  shorts uninstall    Remove everything"
        echo ""
        echo "  shorts setup <IP> [NAME]   First-time setup"
        echo "  shorts add <IP> [NAME]      Add new device"
        echo "  shorts remove <IP>          Remove device"
        echo "  shorts list                  List all devices"
        echo "  shorts connect <IP>          Connect via ADB"
        echo "  shorts enable <IP>           Enable device"
        echo "  shorts disable <IP>          Disable device"
        echo ""
        echo "Quick Start:"
        echo "  shorts setup 192.168.1.100 living-room"
        exit 1
        ;;
esac
