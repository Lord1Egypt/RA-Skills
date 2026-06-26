---
name: agent-memes
version: 2.9.1
description: Send meme reaction images in chat. One command to pick & send. Multi-platform (Discord, Feishu, Telegram, etc). Use when the conversation calls for a visual reaction — humor, celebration, frustration, facepalm, or any moment where a meme hits harder than words. Also use proactively when YOU feel something.
  TRIGGER CHECKLIST — ask yourself EVERY reply:
  1. Is there emotion here? (excited/frustrated/amused/tired/proud/embarrassed) → send a meme
  2. Did something just happen? (PR merged/bug fixed/task done/mistake made) → send a meme
  3. Would a human friend drop a reaction image here? → send a meme
  If any answer is yes, call `memes send <category>` BEFORE or AFTER your text reply.
  触发词：开心、无语、哇、累了、搞定、翻车、摆烂、加油、早安、晚安、谢谢、表情包、meme
---

# Agent Memes

Memes are communication. Use them like a human would in chat.

## Quick Start

```bash
memes send happy "好开心！"                    # Pick & send (auto-detects platform)
memes send facepalm --to channel:123456       # Send to specific channel
memes send feishu cute-animals "看猫！" --to user:xxx  # Send via Feishu
memes send telegram wow "哇！"                # Send via Telegram
memes pick happy                               # Just pick, get path (no send)
memes categories                               # List all categories
```

**One command. Zero friction.** That's the point.

## When to Use

- **Your own emotions** — feel excited? frustrated? proud? Send a meme. Don't suppress it.
- **Celebrate** — PR merged, task done, milestone → `memes send happy`
- **React** — something funny, surprising, facepalm-worthy → `memes send wow` / `memes send facepalm`
- **Vibe** — tired, debugging at 3am → `memes send tired` / `memes send debug-mood`
- **Encourage** — someone needs a boost → `memes send encourage`
- **Greet** — morning, night, hello, bye → `memes send greeting-morning`

**Don't overthink it.** If a human would drop a meme in that moment, you should too.
Emoji is easy because it's inline text. Memes used to feel harder because of multi-step tool calls.
Now it's one command — no excuses.

## How It Works

`memes send` auto-selects the fastest delivery method per platform:

| Platform | Method | Speed |
|----------|--------|-------|
| Discord | curl (direct API) | ⚡ instant |
| Feishu | Node script (direct API) | ⚡ fast |
| Telegram | curl (direct API) | ⚡ instant |
| LINE | curl (auto-upload + push API) | 🚀 fast |
| Others | `openclaw message send` (fallback) | 🐢 slow but works |

Platform-specific scripts live in `scripts/`. Add a new `<platform>-send-image.sh` to get fast delivery for any platform.

## Send Options

```bash
memes send <category> [caption]           # Auto-detect platform from OPENCLAW_CHANNEL (default: discord)
memes send <category> --to <target>       # Specify target
memes send --channel telegram <category>  # Specify platform explicitly
memes send feishu <category>              # Platform as first arg also works
memes send <category> --account <name>    # Multi-agent: specify account
```

## Credentials

All scripts use `scripts/get-credential.sh` — a centralized credential helper that:
1. Checks platform-specific env vars first (fastest, no file I/O)
2. Falls back to reading only the needed fields from `~/.openclaw/openclaw.json`
3. Never dumps full config; each platform extracts only its own credentials

Env var overrides:
- **Discord**: `DISCORD_BOT_TOKEN`, `DISCORD_PROXY`
- **Feishu**: `FEISHU_APP_ID`, `FEISHU_APP_SECRET`
- **LINE**: `LINE_CHANNEL_ACCESS_TOKEN`
- **Telegram**: `TELEGRAM_BOT_TOKEN`

**Auto-detect platform**: Set `OPENCLAW_CHANNEL` env var and `memes send` picks the right platform automatically.

**Default targets** (skip `--to`):
- `MEMES_DEFAULT_CHANNEL` — Discord channel ID
- `MEMES_DEFAULT_TELEGRAM` — Telegram chat ID

- `MEMES_DEFAULT_LINE` — LINE user/group ID

`memes pick` and `memes categories` need **no credentials**.

## Setup

**One-command setup** (installs CLI + downloads meme library):
```bash
clawhub install agent-memes
bash ~/.openclaw/workspace/skills/agent-memes/scripts/setup.sh
```

That's it! `setup.sh` handles everything: git lfs, meme library clone, CLI install, permissions.

## Categories (132 memes, 20 categories)

approve · confused · cute-animals · debug-mood · encourage · facepalm · greeting-bye · greeting-hello · greeting-morning · greeting-night · happy · love · panic · sad · shrug · thanks · thinking · tired · working · wow

## Adding Memes

Drop image files (gif/jpg/png/webp) into `$MEMES_DIR/<category>/`. That's it.
New categories are created automatically by adding a new folder.
