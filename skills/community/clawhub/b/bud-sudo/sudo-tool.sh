#!/bin/bash
# Sudo Tool - Execute commands with superuser privileges
# Uses OpenSSL for password encryption (more reliable than GPG)

set -e

TOOL_DIR="$HOME/.openclaw/sudo-tool"
PW_FILE="$TOOL_DIR/.password.enc"
SALT_FILE="$TOOL_DIR/.salt"

usage() {
    echo "Sudo Tool - Run commands with elevated privileges"
    echo ""
    echo "Usage:"
    echo "  sudo-tool setup              Configure password (one-time)"
    echo "  sudo-tool <command>         Run command with sudo"
    echo "  sudo-tool status            Check if configured"
    echo "  sudo-tool reset             Remove stored password"
    echo ""
    echo "Examples:"
    echo "  sudo-tool apt update"
    echo "  sudo-tool apt install wireguard-tools"
}

ensure_tool_dir() {
    mkdir -p "$TOOL_DIR"
    chmod 700 "$TOOL_DIR"
}

is_configured() {
    [ -f "$PW_FILE" ] && [ -f "$SALT_FILE" ] && [ -s "$PW_FILE" ]
}

setup_password() {
    ensure_tool_dir
    
    echo "🔐 Setting up sudo password (one-time)..."
    echo ""
    echo "⚠️  Your password will be stored encrypted in:"
    echo "   $PW_FILE"
    echo ""
    read -s -p "Enter your sudo password: " PASSWORD
    echo ""
    
    if [ -z "$PASSWORD" ]; then
        echo "❌ Password cannot be empty"
        exit 1
    fi
    
    # Test password first
    if ! echo "$PASSWORD" | sudo -S echo "   ✅ Password verified" 2>/dev/null; then
        echo "❌ Incorrect password"
        exit 1
    fi
    
    # Generate random salt
    SALT=$(openssl rand -hex 32)
    echo "$SALT" > "$SALT_FILE"
    
    # Encrypt and store
    if ! echo "$PASSWORD" | openssl aes-256-cbc -salt -pbkdf2 -out "$PW_FILE" -pass pass:"$SALT" 2>&1; then
        echo "❌ Failed to encrypt password"
        exit 1
    fi
    
    chmod 600 "$PW_FILE"
    chmod 600 "$SALT_FILE"
    echo ""
    echo "✅ Password configured successfully!"
}

get_password() {
    if ! is_configured; then
        echo "❌ Password not configured. Run: sudo-tool setup"
        exit 1
    fi
    
    SALT=$(cat "$SALT_FILE")
    
    local PW
    if ! PW=$(openssl aes-256-cbc -d -pbkdf2 -in "$PW_FILE" -pass pass:"$SALT" 2>/dev/null); then
        echo "❌ Failed to decrypt password"
        exit 1
    fi
    echo "$PW"
}

run_sudo() {
    if ! is_configured; then
        echo "❌ Password not configured. Run: sudo-tool setup"
        exit 1
    fi
    
    local CMD="$*"
    if [ -z "$CMD" ]; then
        echo "❌ No command provided"
        exit 1
    fi
    
    local PW
    if ! PW=$(get_password); then
        echo "❌ Failed to get password"
        exit 1
    fi
    
    # Write password to secure temp file (deleted immediately after)
    local TMPFILE=$(mktemp)
    chmod 600 "$TMPFILE"
    echo "$PW" > "$TMPFILE"
    
    # Run sudo with password from temp file, then delete
    sudo -S bash -c "$CMD" < "$TMPFILE"
    rm -f "$TMPFILE"
}

status() {
    if is_configured; then
        echo "✅ Configured"
        echo "   Password file: $PW_FILE"
    else
        echo "❌ Not configured"
        echo "   Run: sudo-tool setup"
    fi
}

reset() {
    rm -f "$PW_FILE" "$SALT_FILE"
    echo "✅ Password removed"
}

# Parse command
CMD="${1:-}"

case "$CMD" in
    setup)
        setup_password
        ;;
    status)
        status
        ;;
    reset)
        reset
        ;;
    "")
        usage
        ;;
    *)
        if [[ "$CMD" == "setup" || "$CMD" == "status" || "$CMD" == "reset" ]]; then
            echo "Unknown command: $CMD"
            usage
            exit 1
        fi
        shift
        run_sudo "$CMD" "$@"
        ;;
esac