#!/usr/bin/env bash
# notify.sh - Cross-platform notification wrapper
# Created by lobbie 🦞

# Detect OS
OS=$(uname -s 2>/dev/null || echo "Unknown")

if [[ "$OS" == "Darwin" ]]; then
    # macOS
    osascript -e "display alert \"${2:-Lobbie Notification}\" message \"${1:-Notification from lobbie!}\""
elif [[ "$OS" == "Linux" ]]; then
    # Check if we are in WSL
    if grep -qi "Microsoft" /proc/version 2>/dev/null; then
        # WSL: Call Windows powershell for the pop-up
        powershell.exe -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('${1:-Notification from lobbie!}', '${2:-Lobbie Notification}')"
    else
        # Native Linux: use notify-send
        notify-send "${2:-Lobbie Notification}" "${1:-Notification from lobbie!}"
    fi
elif [[ "$OS" == "Unknown" ]] || [[ "$OS" == "MSWindowsNT" ]]; then
    # Windows (via Git Bash/Cygwin/etc)
    powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms. MessageBox]::Show('${1:-Notification from lobbie!}', '${2:-Lobbie Notification}')"
else
    echo "Unsupported OS: $OS"
    exit 1
fi
