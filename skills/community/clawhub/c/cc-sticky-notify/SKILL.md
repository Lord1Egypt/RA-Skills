---
name: cc-sticky-notify
description: >
  Install, configure, or fix cc-sticky-notify — a notification system that displays a pinned yellow sticky note in the Mac top-right corner for key Claude Code events (task completed, permission required, command failed, etc.). No third-party dependencies; uses a native Swift floating window + macOS display notification dual-layer approach, fully self-contained within the skill directory. Use this skill when the user says "install sticky notify", "configure Mac task notifications", "set up Claude Code completion alerts", "sticky notify not working", "reinstall notification hook", etc. Also used for updating scripts or troubleshooting notification failures.
---

# cc-sticky-notify

A pinned sticky note notification system for Mac. Key Claude Code events appear as a **yellow floating sticky note** in the top-right corner, persisting until manually closed.

## File Structure (fully self-contained)

```
~/.claude/skills/cc-sticky-notify/
├── SKILL.md
├── install.sh                   ← one-time setup: chmod + settings.json guidance
└── scripts/
    ├── notify.sh                ← main notification script (called directly by hooks)
    ├── sticky-window.swift      ← Swift source (compiled by install.sh on first install)
    └── sticky-notify.app/       ← .app bundle (built automatically on first use)
        └── Contents/
            ├── Info.plist
            └── MacOS/
                └── sticky-notify-app
```

**Two-layer notification mechanism**:
1. `display notification` — no permissions required, appears instantly in top-right corner
2. Swift NSWindow (`.floating` level) — pinned sticky note, close manually with ✕

**Hook coverage** (consistent with popo-notify):

| Hook | Trigger | Sticky note content |
|------|---------|---------------------|
| `Stop` | Task completed | ✅ Task completed + time/project/session |
| `Notification/permission_prompt` | Permission approval needed | 🔐 Permission approval required |
| `Notification/idle_prompt` | Waiting for user selection | 💬 Awaiting your input |
| `PostToolUse/Bash` (on failure) | Command execution failed | ❌ Command failed, exit code |

---

## Requirements

- **macOS 12 Monterey or later**
- **Xcode Command Line Tools** — required for compiling the Swift floating window, code signing, and JSON parsing

  ```bash
  xcode-select --install
  ```

  All dependencies (`swiftc`, `codesign`) come from Xcode CLT. `install.sh` will check and exit early if CLT is missing.

---

## Installation

When the user requests installation, follow these steps:

### Step 1 — Run install.sh

```bash
bash ~/.claude/skills/cc-sticky-notify/install.sh
```

What this script does:
1. **Check Xcode CLT** — exits early with instructions if `xcode-select -p` fails.
2. **`chmod +x notify.sh`** — ensures the script is executable (git clone may strip the +x bit).
3. **Build `.app bundle`** — compiles `sticky-window.swift`, writes `Info.plist` + entitlements, signs with `codesign`. Skipped if the bundle already exists.
4. **Check hook configuration** — inspects `~/.claude/settings.json` for existing `cc-sticky-notify` entries and prints the required hook commands if none are found.
5. **Smoke test** — fires a test notification via `notify.sh`.

### Step 2 — Configure settings.json hooks

Read `~/.claude/settings.json` and append one sticky-notify entry to each of the following four locations in the `hooks` field (skip if already present).

**Stop** — append to `Stop[0].hooks`:
```json
{
  "type": "command",
  "command": "$HOME/.claude/skills/cc-sticky-notify/scripts/notify.sh"
}
```

**Notification/permission_prompt** — append:
```json
{
  "type": "command",
  "command": "$HOME/.claude/skills/cc-sticky-notify/scripts/notify.sh '🔐 Claude Code Permission approval required, check terminal'"
}
```

**Notification/idle_prompt** — append:
```json
{
  "type": "command",
  "command": "$HOME/.claude/skills/cc-sticky-notify/scripts/notify.sh '💬 Claude Code Awaiting your input, check terminal'"
}
```

**PostToolUse/Bash** — append (triggers only on failure):
```json
{
  "type": "command",
  "command": "bash -c 'INPUT=$(cat); STATUS=$(echo \"$INPUT\" | jq -r \".tool_response.exitCode // 0\"); [ \"$STATUS\" != \"0\" ] && $HOME/.claude/skills/cc-sticky-notify/scripts/notify.sh \"❌ Claude Code Command failed, exit code: $STATUS\" || true'"
}
```

### Step 3 — Verify

```bash
# Test arg mode (simulates Notification hook)
$HOME/.claude/skills/cc-sticky-notify/scripts/notify.sh '✅ Installation verified'

# Test stdin mode (simulates Stop hook)
echo '{"session_id":"test12345678"}' | $HOME/.claude/skills/cc-sticky-notify/scripts/notify.sh
```

A yellow sticky note and system notification appearing in the top-right corner confirms successful installation.

---

## Configuration

### CC_STICKY_NOTIFY_CLOSE_TIMEOUT — Auto-close timeout

Sticky notes automatically close after **1 hour (3600 seconds)** by default. Override with this environment variable:

```bash
export CC_STICKY_NOTIFY_CLOSE_TIMEOUT=300   # auto-close after 5 minutes
```

- Unit: seconds (decimals supported, e.g. `30.5`)
- Must be greater than 0; otherwise falls back to the default 3600 seconds
- Set a large value (e.g. `86400`) to keep the note visible for nearly a full day

To persist the setting, add it to your shell config (`~/.zshrc` or `~/.bashrc`):

```bash
echo 'export CC_STICKY_NOTIFY_CLOSE_TIMEOUT=300' >> ~/.zshrc
```

---

## Troubleshooting

**No system notification either**
- Verify the hooks configuration is correctly written in `~/.claude/settings.json`
- Path should be `$HOME/.claude/skills/cc-sticky-notify/scripts/notify.sh`

**`xcrun: error: invalid active developer path` during compilation**
- Xcode Command Line Tools path is broken (common after macOS upgrade or Xcode reinstall)
- Fix: `sudo xcode-select --reset`
- If that doesn't work, reinstall: `xcode-select --install`
- The floating sticky window will be disabled if swiftc can't compile, but system notifications still work

**`Permission denied` on notify.sh**
- The script is missing execute permission — happens when files are cloned/copied without preserving permissions
- Fix: `chmod +x ~/.claude/skills/cc-sticky-notify/scripts/notify.sh`
- Re-run `install.sh` after fixing (the latest version auto-runs `chmod +x` on startup)
