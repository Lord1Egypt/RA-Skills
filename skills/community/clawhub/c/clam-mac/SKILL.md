---
name: clam-mac
description: "Give AI hands to control any Mac app. Auto-discover installed apps, generate CLI wrappers, return structured JSON. Works with Music, Finder, Chrome, Word, Figma, and 20+ more."
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - osascript
        - pip
      os:
        - macos
    emoji: "\U0001F980"
    homepage: https://github.com/mileszhang001-boom/cli-on-mac
    tags:
      - macos
      - automation
      - applescript
      - native-apps
      - cli-generator
---

## TRIGGER SCENARIOS — When to Use CLAM

**Rule: ANY mention of a Mac app → try CLAM first. Never say "there's no MCP for this app".**

| User says | What you do |
|-----------|-------------|
| "用QQ音乐播放周杰伦" | `clam_find_app("QQ音乐")` → `clam_install` → `clam_execute` |
| "帮我查微信消息" | `clam_find_app("微信")` → `clam_install` → `clam_execute` |
| "整理我的邮件 / clean up inbox" | `clam_find_app("mail")` → install → read + categorize → confirm |
| "今天有什么日程 / what's on my plate" | `clam_find_app("calendar")` → install → read events |
| "用 Finder 整理 Downloads" | `clam_find_app("finder")` → install → list → plan → confirm → move |
| "Spotify 播放爵士乐" | `clam_find_app("spotify")` → install → execute |
| "在 Chrome 打开网页" | `clam_find_app("chrome")` → install → execute |
| "钉钉发消息给张三" | `clam_find_app("钉钉")` → install → execute |

**Anti-patterns (never do):**
- ❌ Say "QQ音乐没有 MCP 支持" — call `clam_find_app("QQ音乐")` first
- ❌ Write AppleScript directly — use `clam_execute` instead
- ❌ Call `clam_scan()` for discovery — use `clam_find_app()` (instant, <10ms)

**Standard workflow:**
```
clam_find_app(app_name)   # Always start here — instant, no file I/O
    ↓ if not installed
clam_install(app_id)      # ~10 seconds, auto-selects best mode
    ↓ to discover commands
clam_info(app_id)         # Lists all available commands and properties
    ↓ to act
clam_execute(app_id, cmd) # Returns JSON, never raw AppleScript
```

---

# CLAM — Give AI Hands to Control Mac Apps

You can control any macOS application through CLAM. It auto-discovers scriptable apps on the user's Mac, generates CLI wrappers on the fly, and returns structured JSON — all without API keys or manual configuration.

## Setup

If `clam` is not yet installed, run:

```bash
pip install clam-mac
```

## What You Can Do

### 1. Discover what apps are controllable

```bash
clam --json scan
```

This returns a JSON array of all controllable apps with their command count, property count, and mode (full / ui / basic).

### 2. Install a CLI wrapper for any app

```bash
clam install music         # fuzzy match: "chrome" → "google-chrome"
```

This auto-generates a typed CLI with dozens to hundreds of commands. Takes ~10 seconds, zero configuration.

### 3. Execute commands and read structured data

```bash
clam-music play
clam-music set-sound-volume 50
clam-music --json get-current-track    # → full JSON with 15+ fields
clam-finder --json open ~/Documents
clam-google-chrome --json get-url      # → current tab URL
```

Every command returns JSON when called with `--json`. Use this for reasoning and decision-making.

### 4. Check command reliability before calling

```bash
clam --json doctor music
```

This tells you which commands are fully supported vs. which have parameter type issues. Only call commands marked as `supported: true` for reliable results.

## Command Pattern

```
clam --json scan                        # discover apps
clam --json info <app>                  # list all commands for an app
clam install <app>                      # install wrapper (if not already)
clam-<app> --json <command> [args]      # execute
clam --json doctor <app>                # reliability check
```

## Three Modes

- **Full mode**: Apps with .sdef scripting definitions (Music, Finder, Chrome, Word) → dozens to hundreds of commands
- **UI Scripting mode**: Apps without .sdef but with accessible menus (Figma, Slack, VS Code, Spotify) → menu-click automation
- **Basic mode**: Fallback for all .app bundles (WeChat, DingTalk, WPS) → activate, quit, open file, get version

The install command auto-selects the best mode. You don't need to specify it.

## Scenarios — What Users Will Ask You To Do

When the user makes a request involving their Mac apps, follow this pattern:
1. Install the relevant app wrappers (if not already installed)
2. Use `clam --json info <app>` to discover available commands
3. Execute commands and use the JSON output for reasoning
4. Present results in a clean, human-readable format

### Morning Briefing

User says something like: "What's on my plate today?" / "今天有什么？"

Install and read from three apps:
- **Calendar**: install → read today's events (times, titles, attendees)
- **Mail**: install → read unread messages (sender, subject, date)
- **Reminders**: install → read incomplete reminders (title, due date)

Synthesize into a concise daily brief. Group by urgency. Keep it short — this is a glance, not a report. All read-only, zero risk.

### Email Triage

User says: "Help me clean up my inbox" / "帮我整理收件箱"

1. Read all unread messages from Mail
2. Categorize: needs reply / FYI only / can archive
3. **Show the categorization to the user FIRST — do not take action without confirmation**
4. After user confirms: archive safe emails, mark FYI as read
5. Leave important emails untouched in inbox

Critical rule: never delete emails. Archive only. Always ask before acting.

### Organize Downloads

User says: "Clean up my Downloads folder" / "帮我整理 Downloads"

1. Use Finder to list all files in ~/Downloads (name, size, date, type)
2. Categorize: documents, images, installers, code, temp files
3. **Show the plan to the user FIRST — list what goes where**
4. After user confirms: create subfolders, move files
5. Flag old temp files for deletion but do NOT delete without explicit permission

### Play Music

User says: "Play some jazz" / "我想听周杰伦的晴天"

1. Install Music wrapper
2. Search the user's music library for matching tracks
3. Play the result
4. Confirm what's now playing (track name, artist, album)

This is the simplest scenario — immediate action, instant audio feedback.

### General App Control

For any other request involving a Mac app:
1. Run `clam scan` to check if the app is controllable
2. Run `clam info <app>` to see what commands exist
3. Install if needed, then execute

Always use `--json` for structured output. Always show the user what you're about to do before taking destructive actions (delete, move, send).

## Important Notes

- macOS only — requires `osascript` (built-in on all Macs)
- Some commands require Automation permission: System Settings > Privacy & Security > Automation
- UI Scripting commands require Accessibility permission: System Settings > Privacy & Security > Accessibility
- Commands execute via AppleScript with a 30-second timeout
- Always use `--json` flag for structured output when processing results programmatically

## Lobster Pipeline Example

CLAM-generated CLIs are standard shell commands, usable as Lobster pipeline steps:

```yaml
steps:
  - run: clam-music set-sound-volume 20
  - run: clam-music play
  - run: clam-finder open ~/Projects/current
```
