#!/bin/bash
# Screenshot utility for screen-vision skill
# Auto-detects platform and captures screenshot
# Usage: screenshot.sh [output_path] [display_id]

OUTPUT="${1:-/tmp/sv_screenshot.png}"
DISPLAY_ID="${2:-}"

detect_and_capture() {
    case "$(uname -s)" in
        Linux*)
            local display="${DISPLAY_ID:-$DISPLAY}"
            if [ -z "$display" ]; then
                # Try to find active display
                display=$(ls /tmp/.X11-unix/ 2>/dev/null | head -1 | sed 's/X/:/')
                [ -z "$display" ] && display=":1"
            fi
            DISPLAY="$display" scrot -z -overwrite "$OUTPUT" 2>/dev/null && return 0
            
            # Fallback: use xdotool + import (ImageMagick)
            DISPLAY="$display" import -window root "$OUTPUT" 2>/dev/null && return 0
            
            # Fallback: use Python
            python3 -c "
import subprocess
subprocess.run(['DISPLAY', '$display', 'scrot', '-z', '-overwrite', '$OUTPUT'], env={'DISPLAY': '$display', 'PATH': '/usr/bin:/bin'})
" 2>/dev/null && return 0
            
            echo "ERROR: No screenshot tool available on Linux" >&2
            return 1
            ;;
        Darwin*)
            screencapture -x "$OUTPUT" 2>/dev/null && return 0
            echo "ERROR: screencapture failed" >&2
            return 1
            ;;
        MINGW*|MSYS*|CYGWIN*)
            python3 -c "
import pyautogui
pyautogui.screenshot('$OUTPUT')
" 2>/dev/null && return 0
            echo "ERROR: pyautogui screenshot failed" >&2
            return 1
            ;;
        *)
            echo "ERROR: Unsupported OS" >&2
            return 1
            ;;
    esac
}

detect_and_capture
exit $?
