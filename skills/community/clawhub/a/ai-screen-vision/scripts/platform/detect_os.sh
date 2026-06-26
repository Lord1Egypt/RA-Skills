#!/bin/bash
# Platform detection for screen-vision skill
# Output: OS name, display environment, available tools

set -e

detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="linux";;
        Darwin*)    OS="macos";;
        MINGW*|MSYS*|CYGWIN*) OS="windows";;
        *)          OS="unknown";;
    esac
    echo "$OS"
}

check_linux_desktop() {
    if [ -n "$DISPLAY" ]; then
        echo "desktop"
    elif [ -n "$WAYLAND_DISPLAY" ]; then
        echo "wayland"
    else
        echo "headless"
    fi
}

check_tools() {
    local os="$1"
    local missing=()
    
    case "$os" in
        linux)
            for tool in scrot xdotool; do
                command -v "$tool" &>/dev/null || missing+=("$tool")
            done
            ;;
        macos)
            for tool in cliclick screencapture; do
                command -v "$tool" &>/dev/null || missing+=("$tool")
            done
            ;;
        windows)
            python3 -c "import pyautogui" 2>/dev/null || missing+=("pyautogui")
            ;;
    esac
    
    if [ ${#missing[@]} -eq 0 ]; then
        echo "ready"
    else
        echo "missing:${missing[*]}"
    fi
}

# Main
OS=$(detect_os)
echo "OS=$OS"

if [ "$OS" = "linux" ]; then
    MODE=$(check_linux_desktop)
    echo "MODE=$MODE"
fi

STATUS=$(check_tools "$OS")
echo "TOOLS=$STATUS"

# Python check
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
fi
echo "PYTHON=$PYTHON"

# Screen resolution
case "$OS" in
    linux)
        if [ "$MODE" != "headless" ]; then
            RES=$(xdpyinfo 2>/dev/null | grep dimensions | head -1 | awk '{print $2}')
            echo "RESOLUTION=$RES"
        fi
        ;;
    macos)
        RES=$(system_profiler SPDisplaysDataType 2>/dev/null | grep Resolution | head -1 | awk '{print $2"x"$4}')
        echo "RESOLUTION=$RES"
        ;;
esac
