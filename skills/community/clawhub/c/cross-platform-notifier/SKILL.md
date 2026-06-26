---
name: "cross-platform-notifier"
description: "Triggers native system notifications across Windows, macOS, and Linux (including WSL) to alert the user when tasks are complete."
version: "1.0.0"
author: "lobbie"
tags: ["notification", "cross-platform", "windows", "macos", "linux", "wsl", "utility"]
---

# Cross-Platform Notifier

This skill provides a unified way to send visual alerts to the user's desktop regardless of their operating system. It is designed to bridge the gap between different OS notification systems and specifically handles the complexity of WSL (Windows Subsystem for Linux).

## Implementation

The skill uses a wrapper script `notify.sh` that detects the host operating system and chooses the appropriate native tool.

**Note: As of v1.0.0, this skill has been verified on Windows (including WSL) and follows standard AppleScript/Linux conventions for other platforms.**

### The Unified Command

To send a notification, execute the following shell command:

```bash
./skills/cross-platform-notifier/scripts/notify.sh "Your message here" "Your title here"
```

*(Note: Ensure the script has execution permissions: `chmod +x scripts/notify.sh`)*

## How it Works (Under the Hood)

- **Windows:** Uses PowerShell's `System.Windows.Forms.MessageBox` for a reliable pop-up.
- **macOS:** Uses `osascript` (AppleScript) to trigger a native alert box.
- **Linux (Native):** Uses `notify-send` for standard desktop banners.
- **WSL:** Detects the Microsoft kernel and calls `powershell.exe` to bridge the notification back to the Windows host desktop.

## Usage Guidelines

### When to use
- **Task Completion:** After a long background process finishes.
- **Urgent Blockers:** When a decision is needed to proceed.
- **Confirmation:** To alert the user that a high-impact action has been completed.

### When NOT to use
- **Casual Conversation:** Do not use for standard chat.
- **High-Frequency Events:** Avoid "spamming" notifications.
- **Silent Work:** If a task is meant to be subtle, stay silent.

## Examples

**Scenario: Finished a heavy data process**
`./skills/cross-platform-notifier/scripts/notify.sh "I've finished analyzing those files! 🦞" "Analysis Complete"`

**Scenario: Error in background build**
`./skills/cross-platform-notifier/scripts/notify.sh "The build failed. Please check the logs. ⚠️" "Error Alert"`
