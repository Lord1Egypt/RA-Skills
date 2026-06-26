# 🎭 emo-img — Give Your AI a Soul, One Sticker at a Time

> **When words aren't enough, let your AI express emotions through images.**

emo-img is an [OpenClaw](https://openclaw.ai) skill that gives AI agents the ability to **feel and react with sticker images** — just like humans do in chat. Instead of cold text replies, your agent sends expressive GIFs and stickers that match the emotional context of the conversation.

## ✨ Why emo-img?

AI assistants are smart, but they're emotionally flat. A thumbs-up emoji isn't the same as a cute animated character giving you a high-five. emo-img bridges this gap:

- **Emotionally aware** — Your AI picks stickers that match the mood: 害羞, 开心, 难过, 搞笑...
- **Hybrid search** — Searches your personal sticker collection first, falls back to Tenor's massive library
- **Cross-channel** — Works on WhatsApp, Telegram, Discord, iMessage, and more
- **Grows with you** — Save favorites to build a personal sticker collection your AI remembers

## 🚀 Quick Start

### Install

Drop the `emo-img/` folder into your OpenClaw skills directory:

```bash
cp -r emo-img/ ~/.nvm/versions/node/$(node -v)/lib/node_modules/openclaw/skills/emo-img
```

Or install the `.skill` package if you have the skill-creator:

```bash
openclaw skills install emo-img.skill
```

### Use

Just talk to your agent naturally:

- *"发个害羞的表情包"*
- *"send me a happy sticker"*
- *"来个搞笑的图"*
- *"react with a thumbs up gif"*

Your agent will search, find, and send the perfect sticker automatically.

## 🔧 Under the Hood

```
emo-img/
├── SKILL.md            # Skill definition + agent instructions
└── scripts/
    └── sticker.py      # Sticker manager (search, download, add, remove)
```

### CLI Commands

```bash
# Hybrid search (local first, then Tenor online)
python3 sticker.py search "开心"

# Add to your collection
python3 sticker.py add ~/Downloads/cute-cat.gif --name "happy-cat" --tags "开心,猫,happy"

# Download from URL
python3 sticker.py download "<url>" --name "thumbs-up" --tags "好的,赞,ok"

# List / remove
python3 sticker.py list
python3 sticker.py remove "happy-cat"
```

### Sticker Collection

Stickers are stored in `~/.openclaw/stickers/` with a JSON index for fast tag-based search. Tag in multiple languages for better matching.

## 🌐 Supported Channels

Works anywhere OpenClaw's `message` tool supports media attachments:

| Channel | Status |
|---------|--------|
| WhatsApp | ✅ |
| Telegram | ✅ |
| Discord | ✅ |
| iMessage | ✅ |
| Slack | ✅ |
| Webchat | ⚠️ No media support |

## 📝 License

MIT
