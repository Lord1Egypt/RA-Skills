---
name: screencli-record
description: |
  Record AI-driven browser demos with screencli. One command creates a polished
  screen recording with gradient backgrounds, auto-zoom, click highlights, and
  cursor trails — then uploads it to a shareable link. Use when the user wants
  to record a demo, screencast, walkthrough, or video of a web app.
license: MIT
compatibility: Requires Node.js 18+ and FFmpeg. Works on macOS, Linux, Windows.
metadata:
  author: danleshem
  version: "1.0"
  website: https://screencli.sh
---

## What It Does

screencli records an AI-driven browser session and produces a polished MP4 with gradient backgrounds, auto-zoom, click highlights, and cursor trails. The AI agent navigates the target URL following your prompt instructions, then the recording is composed with effects and auto-uploaded to screencli.sh with a shareable link. No video editing needed.

## When to Use This Skill

Use this skill when the user asks to:

- **Record a demo or walkthrough** of a web app, feature, or workflow
- **Create a screencast or video** showing how something works in a browser
- **Generate a shareable link** to a screen recording
- **Make a GIF or video** for a README, PR, docs, or social media
- **Record a before/after** to show a UI change or bug fix
- **Demo a deploy or staging environment** visually

Do **not** use this skill for:
- Screenshots (use a screenshot tool instead)
- Non-browser tasks (terminal recordings, desktop apps)
- Editing existing videos

## Quick Start

Record a demo and get a shareable link:

```
npx screencli record https://example.com -p "Click the Sign Up button, fill in the form with test data, and submit"
```

On first run, the CLI opens a browser for GitHub login automatically. After that, it records the session, applies effects, uploads, and prints a shareable URL.

## Recording

### Command

```
npx screencli record [url] -p "<prompt>" [options]
```

The URL and prompt are required. If omitted, the CLI prompts interactively.

### Key Options

| Flag | Default | Description |
|------|---------|-------------|
| `-p, --prompt <text>` | *(required)* | Instructions for the AI agent |
| `--background <name>` | auto | Override gradient: `midnight`, `ember`, `forest`, `nebula`, `slate`, `copper` |
| `--viewport <WxH>` | `1920x1080` | Browser viewport dimensions |
| `--login` | off | Open browser for manual login before AI takes over |
| `--auth <name>` | — | Save/load auth state by name |
| `--local` | off | Skip cloud upload |
| `--unlisted` | off | Upload as unlisted (not on public profile) |
| `--max-steps <n>` | `50` | Maximum agent iterations |
| `--padding <percent>` | `8` | Background padding (0-50%) |
| `--corner-radius <px>` | `12` | Video corner radius |
| `--no-shadow` | off | Disable drop shadow |
| `-m, --model <model>` | `claude-sonnet-4-20250514` | Claude model to use |
| `--slow-mo <ms>` | `0` | Extra delay between actions |
| `-o, --output <dir>` | `./recordings` | Output directory |
| `-v, --verbose` | off | Debug logging |

### Examples

**Simple — record a public page:**

```
npx screencli record https://myapp.com -p "Navigate to the pricing page and compare the Free and Pro plans"
```

**With auth — login to a private app first:**

```
# First run: human logs in, auth state saved
npx screencli record https://app.internal.com -p "Show the dashboard metrics" --login --auth myapp

# Next runs: reuses saved session
npx screencli record https://app.internal.com -p "Export the monthly report" --auth myapp
```

## Exporting

Export a recording with platform-specific presets:

```
npx screencli export <recording-dir> --preset <name>
```

### Presets

| Preset | Resolution | Aspect | Format | Max Duration |
|--------|-----------|--------|--------|--------------|
| `youtube` | 1920x1080 | 16:9 | mp4 | — |
| `twitter` | 1280x720 | 16:9 | mp4 | 140s |
| `instagram` | 1080x1920 | 9:16 | mp4 | 90s |
| `tiktok` | 1080x1920 | 9:16 | mp4 | — |
| `linkedin` | 1080x1080 | 1:1 | mp4 | — |
| `github-gif` | 800x450 | 16:9 | gif | 12s |

### Example

```
npx screencli export ./recordings/abc123 --preset twitter
```

Export also accepts `--background`, `--padding`, `--corner-radius`, `--no-shadow`, `--no-zoom`, `--no-highlight`, and `--no-cursor`.

## Auth for Private Apps

To record behind a login wall, use `--login` and `--auth` together on the first run:

```
npx screencli record https://app.example.com -p "..." --login --auth myapp
```

The browser opens for you to log in manually. Once done, the AI agent takes over and auth state is saved to `~/.screencli/auth/myapp.json`.

On subsequent runs, pass just `--auth`:

```
npx screencli record https://app.example.com -p "..." --auth myapp
```

If a session expires, re-run with `--login --auth <name>` to refresh it.

## Cloud

Recordings auto-upload to screencli.sh by default. Skip with `--local`.

### Commands

| Command | Description |
|---------|-------------|
| `npx screencli login` | Sign in to screencli cloud |
| `npx screencli logout` | Sign out |
| `npx screencli whoami` | Show current user, plan, and credits |
| `npx screencli recordings` | List your recordings with links |
| `npx screencli upload <dir>` | Upload a local recording to the cloud |
| `npx screencli delete <id>` | Delete a cloud recording |
| `npx screencli render <id>` | Re-render on the cloud with different background/preset |

### Credits

1 credit = 10 agent steps. Free tier includes 15 credits/month.

After a recording uploads, the CLI shows credits used and remaining.

## Effects

All recordings get automatic post-processing:

- **Gradient background** — automatically selected (override with `--background <name>`)
- **Auto-trim** — removes idle time between actions
- **Auto-zoom** — zooms into the active area during interactions
- **Click highlights** — visual pulse on each click
- **Cursor trail** — smooth cursor movement overlay

Toggle individual effects off with `--no-zoom`, `--no-highlight`, `--no-cursor`.

See [references/effects.md](references/effects.md) for gradient colors and the full effects pipeline.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Not logged in | Run `npx screencli record` — login is triggered automatically |
| FFmpeg missing | `brew install ffmpeg` (macOS) or see ffmpeg.org |
| Auth expired | Re-run with `--login --auth <name>` |
| Agent stuck or looping | Refine prompt, lower `--max-steps` |
| Recording too long | Use `--max-steps` to limit, or be more specific in prompt |
| Upload failed | Check `npx screencli whoami` for credits, retry with `npx screencli upload <dir>` |

## References

- [CLI Reference](references/cli-reference.md) — all commands and flags
- [Effects Reference](references/effects.md) — gradients, backgrounds, effects pipeline
