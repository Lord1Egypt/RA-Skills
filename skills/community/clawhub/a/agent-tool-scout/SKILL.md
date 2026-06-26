---
name: clam-mac
description: "Give AI hands to control any Mac app. Auto-discover installed apps, generate CLI wrappers, return structured JSON. Works with Music, Finder, Chrome, Word, Figma, and 20+ more."
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - osascript
        - pip
      os:
        - macos
    emoji: "🦀"
    homepage: https://github.com/mileszhang001-boom/cli-on-mac
    tags:
      - macos
      - automation
      - applescript
      - native-apps
      - cli-generator
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
