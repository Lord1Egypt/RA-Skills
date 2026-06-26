#!/bin/bash
# Clipboard Manager - Cross-platform clipboard handling
# Version: 1.0.0

CLIPBOARD_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
HISTORY_FILE="$CLIPBOARD_DIR/clipboard-history.md"
MAX_HISTORY=50

# Initialize history file
init_history() {
    if [ ! -f "$HISTORY_FILE" ]; then
        echo "# Clipboard History" > "$HISTORY_FILE"
        echo "" >> "$HISTORY_FILE"
    fi
}

# Get OS type
get_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos";;
        Linux*)     echo "linux";;
        MINGW*|MSYS*|CYGWIN*) echo "windows";;
        *)          echo "unknown";;
    esac
}

# Copy to system clipboard
copy_to_clipboard() {
    local text="$1"
    local os=$(get_os)
    
    case "$os" in
        macos)
            echo "$text" | pbcopy
            ;;
        linux)
            if command -v xclip &> /dev/null; then
                echo "$text" | xclip -selection clipboard
            elif command -v xsel &> /dev/null; then
                echo "$text" | xsel --clipboard
            fi
            ;;
        windows)
            echo "$text" | clip
            ;;
    esac
}

# Get system clipboard content
get_clipboard() {
    local os=$(get_os)
    
    case "$os" in
        macos)
            pbpaste
            ;;
        linux)
            if command -v xclip &> /dev/null; then
                xclip -selection clipboard -o
            elif command -v xsel &> /dev/null; then
                xsel --clipboard -o
            fi
            ;;
        windows)
            powershell -command "Get-Clipboard"
            ;;
    esac
}

# Save clipboard to history
save_clipboard() {
    init_history
    local content=$(get_clipboard)
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    local count=$(grep -c "^## \[" "$HISTORY_FILE" 2>/dev/null || echo "0")
    local index=$((count + 1))
    
    # Truncate content for display
    local preview=$(echo "$content" | head -c 50 | tr '\n' ' ')
    
    {
        echo ""
        echo "## [$index] $timestamp"
        echo "\`\`\`"
        echo "$content"
        echo "\`\`\`"
        echo ""
    } >> "$HISTORY_FILE"
    
    # Trim old entries if over limit
    trim_history
    
    echo "✅ Clipboard saved as #$index"
    echo "   Preview: $preview..."
}

# Trim history to max entries
trim_history() {
    local count=$(grep -c "^## \[" "$HISTORY_FILE" 2>/dev/null || echo "0")
    if [ "$count" -gt "$MAX_HISTORY" ]; then
        # Keep only last MAX_HISTORY entries (simplified)
        head -n 20 "$HISTORY_FILE" > "$HISTORY_FILE.tmp"
        tail -n $((count * 5)) "$HISTORY_FILE" >> "$HISTORY_FILE.tmp"
        mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"
    fi
}

# Show history
show_history() {
    local limit="${1:-10}"
    init_history
    echo "📋 Clipboard History (last $limit):"
    echo ""
    grep "^## \[" "$HISTORY_FILE" | tail -n "$limit"
}

# Search history
search_history() {
    local keyword="$1"
    init_history
    echo "🔍 Searching clipboard history for: $keyword"
    echo ""
    grep -A 2 -B 1 -i "$keyword" "$HISTORY_FILE" | head -50
}

# Clear history
clear_history() {
    echo "# Clipboard History" > "$HISTORY_FILE"
    echo "" >> "$HISTORY_FILE"
    echo "✅ Clipboard history cleared"
}

# Set clipboard content
set_clipboard() {
    local text="$1"
    copy_to_clipboard "$text"
    echo "✅ Copied to clipboard"
}

# Get clipboard content
get_clipboard_content() {
    local content=$(get_clipboard)
    echo "📋 Current Clipboard:"
    echo "\`\`\`"
    echo "$content"
    echo "\`\`\`"
}

# Show help
show_help() {
    echo "Clipboard Manager - Cross-platform clipboard handling"
    echo ""
    echo "Usage:"
    echo "  clipboard.sh save          - Save current clipboard to history"
    echo "  clipboard.sh get           - Show current clipboard content"
    echo "  clipboard.sh set \"<text>\"  - Set clipboard content"
    echo "  clipboard.sh history [n]   - Show last n entries (default: 10)"
    echo "  clipboard.sh search \"<k>\"  - Search history"
    echo "  clipboard.sh clear         - Clear history"
    echo ""
}

# Main
case "$1" in
    save)
        save_clipboard
        ;;
    get)
        get_clipboard_content
        ;;
    set)
        set_clipboard "$2"
        ;;
    history)
        show_history "${2:-10}"
        ;;
    search)
        search_history "$2"
        ;;
    clear)
        clear_history
        ;;
    *)
        show_help
        ;;
esac
