#!/bin/bash
# Extension Host restart script
# Restart must be done through UI interaction (CLI has no command execution flag).

# Method 1: AppleScript (macOS)
if [ "$(uname)" = "Darwin" ]; then
    echo "Attempting Extension Host restart via AppleScript..."
    osascript -e '
    tell application "System Events"
        keystroke "p" using {command down, shift down}
        delay 0.3
        keystroke "Developer: Restart Extension Host"
        delay 0.2
        key code 36
    end tell
    ' 2>/dev/null && exit 0
fi

echo "Please restart Extension Host manually:"
echo "  Cmd+Shift+P > 'Developer: Restart Extension Host'"
exit 1
