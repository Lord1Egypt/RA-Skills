# 🎭 Agent Memes

Meme reaction images for AI agents. One command to pick & send across platforms.

```bash
memes send happy "好开心！"           # Discord (default)
memes send feishu wow "哇！" --to user:xxx  # Feishu
memes send telegram happy --to 12345  # Telegram
memes send facepalm                  # Auto-detects platform via OPENCLAW_CHANNEL
```

## Why?

Because emoji is easy (inline text) but memes used to require 3 tool calls.
Now it's one command. **Zero friction = more memes = better vibes.**

## Install

### Via ClawHub (recommended)

```bash
npm i -g clawhub
clawhub install agent-memes
```

### Manual

```bash
# 1. Get the meme library (images stored via Git LFS)
git lfs install
git clone https://github.com/kagura-agent/memes ~/.openclaw/workspace/memes

# 2. Install CLI
sudo cp scripts/memes.sh /usr/local/bin/memes
chmod +x /usr/local/bin/memes
```

## Usage

```bash
memes send <category> [caption] [--to target] [--channel platform]
memes pick <category>       # Just pick, no send
memes categories            # List all categories
```

Auto-detects platform from `OPENCLAW_CHANNEL` env var. Set `MEMES_DEFAULT_CHANNEL` (Discord) or `MEMES_DEFAULT_TELEGRAM` to skip `--to`.

## Multi-Platform

| Platform | Method | Speed |
|----------|--------|-------|
| Discord | Direct API (curl) | ⚡ instant |
| Feishu | Direct API (Node) | ⚡ fast |
| Telegram | Direct API (curl) | ⚡ instant |
| Others | OpenClaw CLI fallback | works everywhere |

Add your own platform: drop a `<platform>-send-image.sh` in `scripts/`.

## Categories (97 memes)

approve · confused · cute-animals · debug-mood · encourage · facepalm · greeting-bye · greeting-hello · greeting-morning · greeting-night · happy · love · panic · sad · thanks · thinking · tired · wow

## For OpenClaw Users

This is also available as a skill. See `SKILL.md` for integration details.

## License

MIT