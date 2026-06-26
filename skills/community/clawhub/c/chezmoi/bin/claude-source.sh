#!/bin/bash
# SourceGit Custom Action: Launch Claude Code with a specific folder added

REPO="$1"
CMD="cd \$HOME/works/.vscode && claude --add-dir '$REPO' --dangerously-skip-permissions --resume"

run_terminal() {
    osascript -e "tell app \"Terminal\" to activate"
    osascript -e "tell app \"Terminal\" to do script \"$CMD\""
}

run_tabby() {
    osascript <<EOF
tell application "Tabby"
    activate
    delay 0.3
end tell
tell application "System Events"
    tell process "Tabby"
        keystroke "t" using command down
        delay 0.2
        keystroke "$CMD"
        key code 36
    end tell
end tell
EOF
}

# Run Tabby if installed, otherwise fallback to Terminal
if open -Ra "Tabby" 2>/dev/null; then
    run_tabby
else
    run_terminal
fi
