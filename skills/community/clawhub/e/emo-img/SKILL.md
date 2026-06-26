---
name: emo-img
description: Send sticker/emoji images (表情包) in chat. Search local collection or online (Tenor), download favorites, and send via any channel (WhatsApp, Discord, iMessage, Telegram). Use when the user wants to send a sticker, emoji image, meme, or 表情包.
metadata:
  {
    "openclaw":
      {
        "emoji": "😎",
        "requires": { "bins": ["python3"] },
      },
  }
---

# emo-img — Sticker / Emoji Image Skill

Send sticker images (表情包) in chat conversations. Hybrid search: local collection first, then Tenor online.

## Storage

- Sticker collection: `~/.openclaw/stickers/`
- Index file: `~/.openclaw/stickers/index.json`
- Override with `STICKER_DIR` env var

## Commands

### Search (hybrid: local first, then online)

```bash
python3 {baseDir}/scripts/sticker.py search "开心"
python3 {baseDir}/scripts/sticker.py search "thumbs up" --limit 3
```

Returns JSON with `local` and `online` arrays. Local results have a `file` path; online results have a `url`.

### Search local only

```bash
python3 {baseDir}/scripts/sticker.py search-local "哭"
```

### Search online only (Tenor)

```bash
python3 {baseDir}/scripts/sticker.py search-online "excited" --limit 5
```

### Add a local file

```bash
python3 {baseDir}/scripts/sticker.py add /path/to/sticker.gif --name "happy-cat" --tags "开心,猫,happy,cat"
```

### Download from URL and save

```bash
python3 {baseDir}/scripts/sticker.py download "<url>" --name "thumbs-up" --tags "好的,赞,ok"
```

### List all stickers

```bash
python3 {baseDir}/scripts/sticker.py list
```

### Remove a sticker

```bash
python3 {baseDir}/scripts/sticker.py remove "happy-cat"
```

## Sending Stickers

Use the `message` tool with the `media` field to send sticker images. This works for ALL channels (WhatsApp, Telegram, Discord, etc.) — no external CLI needed.

```json
{
  "action": "send",
  "channel": "<current_channel>",
  "to": "<recipient>",
  "message": "",
  "media": "<sticker_file_path>"
}
```

The `media` field accepts local file paths directly (e.g. `/Users/.../.openclaw/stickers/bocchi-shy.gif`).

For online results not yet downloaded, first run `download` to save locally, then send the saved file path.

## Workflow

1. User says something like "发个表情包" or "send a sticker about X"
2. Run `search "<keyword>"` to find matching stickers
3. If local results exist, use the `file` path directly
4. If only online results, download first with `download`, then use the saved file path
5. Send via the appropriate channel (auto-detect from conversation context)
6. Optionally ask user if they want to save an online sticker to local collection

## Tips

- Tag stickers in both Chinese and English for better search
- Use `--tags` with comma-separated keywords when adding stickers
- The Tenor demo API key has rate limits; set `TENOR_API_KEY` env for heavy use
