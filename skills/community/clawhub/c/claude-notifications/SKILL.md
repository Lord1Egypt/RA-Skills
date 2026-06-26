---
name: claude-notifications
description: "Set up native macOS notifications for Claude Code on local and devpod/remote environments. Use when the user asks to 'setup notifications', 'configure devpod notifications', 'get notified when Claude needs attention', 'setup claude alerts', or 'install notification hooks'. Handles local terminal-notifier, SSH reverse tunnel for devpods, launchd listener, tmux passthrough, and Claude Code hook configuration."
---

# Claude Code Notifications Setup

Set up native macOS notifications for Claude Code — works both locally and on remote devpods via SSH reverse tunnel. Get alerts with sound whenever Claude needs permission, is waiting for input, or requires MCP interaction.

## What It Does

- **Local**: Uses `terminal-notifier` for native macOS notifications when Claude needs permission, goes idle, or requires MCP input
- **Devpod**: Routes notifications from remote devpods through an SSH reverse tunnel to the local `terminal-notifier`, with OSC 9 fallback
- **Hooks**: Configures Claude Code `Notification` hooks for `permission_prompt`, `idle_prompt`, and `elicitation_dialog`

## Platform

**macOS only.** The setup script will exit with a clear error if run on Linux/devpod. It uses `brew`, `launchctl`, and `terminal-notifier` — all macOS-only. The script SSHs into devpods to configure them remotely, so devpod setup is also done from your Mac.

## Important: Run on Local Mac Only

**Always confirm the user is running this on their local Mac, NOT on a devpod.** The entire setup — including devpod configuration — is done from the local machine via SSH. The script SSHs into devpods to configure them remotely. If the user is on a devpod, ask them to switch to their local Mac terminal first.

## Setup Workflow

### 1. Ask for devpod SSH hosts

Ask the user which devpod(s) to configure. Example hosts: `username.devpod-ind`, `username-web.devpod-ind`. If local-only setup, skip devpod args.

### 2. Run the setup script

```bash
# Local only
python3 scripts/setup_notifications.py

# Local + devpods
python3 scripts/setup_notifications.py --devpod <host1> --devpod <host2>
```

Run from the skill's directory: `~/.claude/skills/claude-notifications/`

The script handles:
- Installs `terminal-notifier` via brew if missing
- Copies `notify.py` to `~/.claude/scripts/`
- Creates and starts the reverse tunnel listener (`notify-listener.py`) via launchd
- Adds `RemoteForward 19876` to `~/.ssh/config` for each devpod
- Copies `notify.py` to each devpod and configures Claude Code hooks there
- Adds `set -g allow-passthrough on` to each devpod's `~/.tmux.conf`
- Configures Claude Code notification hooks in `~/.claude/settings.json`
- Sends a test notification

### 3. Remind user of manual steps

After the script completes, **always** tell the user these required manual steps:

1. **Enable notifications for your terminal** in System Settings > Notifications > [Warp / iTerm / Terminal]. Ensure "Allow Notifications" is ON and alert style is "Alerts" or "Banners".
2. **Enable notifications for Script Editor** in System Settings > Notifications > Script Editor (terminal-notifier routes through it).
3. **Turn off Do Not Disturb** or add "Script Editor" and your terminal app to Focus exceptions.
4. **Reconnect SSH sessions** to devpods — existing sessions don't have the reverse tunnel. New sessions get it automatically.

## Architecture

```
┌─────────────────────────────────────────────────┐
│ Devpod (remote)                                 │
│                                                 │
│  Claude Code hook → notify.py                    │
│    → curl localhost:19876 (reverse tunnel)       │
│    → fallback: OSC 9 escape sequence            │
└──────────────────┬──────────────────────────────┘
                   │ SSH RemoteForward 19876
┌──────────────────▼──────────────────────────────┐
│ Local Mac                                       │
│                                                 │
│  notify-listener.py (launchd, port 19876)       │
│    → terminal-notifier → macOS Notification Center│
└─────────────────────────────────────────────────┘
```

## Troubleshooting

- **No notifications showing**: Check System Settings > Notifications for both your terminal app AND "Script Editor" — both must have notifications enabled
- **Do Not Disturb blocking**: Add "Script Editor" to Focus exceptions, or disable DND
- **Listener not running**: `launchctl list | grep claude` and `lsof -i :19876`
- **Restart listener**: `launchctl unload ~/Library/LaunchAgents/com.claude.notify-listener.plist && launchctl load ~/Library/LaunchAgents/com.claude.notify-listener.plist`
- **Listener logs**: `cat ~/.claude/logs/notify-listener.log`
- **Test locally**: `python3 ~/.claude/scripts/notify.py "test" --title "Claude Code" --sound "Glass"`
- **Test devpod tunnel**: From devpod tmux session: `python3 ~/.claude/scripts/notify.py "test" --title "Claude Code" --sound "Glass"`
- **Debug mode**: `DEBUG=1 python3 ~/.claude/scripts/notify.py "test"`
