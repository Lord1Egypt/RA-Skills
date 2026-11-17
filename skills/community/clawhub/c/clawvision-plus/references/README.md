# ClawVision Plus

Plugin for [ClawVision](https://github.com/monaxamo/clawvision) that adds three extra outputs:

- **PDF export** — print-ready PDF with one page per tab.
- **OG image** — 1200×630 social preview PNG.
- **Telegram sharing** — send the OG image + summary caption to a channel or chat.

## Requirements

- Python 3.10+
- `playwright` (already required by ClawVision)
- `Pillow` (`pip install Pillow`)
- `reportlab` (`pip install reportlab`)
- `python-telegram-bot` (only for Telegram sharing: `pip install python-telegram-bot`)

## Usage

First generate a ClawVision summary as usual:

```bash
python ../scripts/generate_visual.py \
  --summary summary.json \
  --output ./out \
  --png --md --pptx \
  --lang en
```

Then run ClawVision Plus on the same output directory:

```bash
python scripts/extend_visual.py \
  --summary summary.json \
  --output ./out \
  --pdf --og \
  --telegram \
  --telegram-chat-id "@your_channel" \
  --telegram-bot-token "YOUR_BOT_TOKEN"
```

## Outputs

- `out/<slug>.pdf` — multi-page PDF export, one page per ClawVision tab.
- `out/<slug>_og.png` — 1200×630 social preview image.
- Telegram message — OG image + caption (or photo + separate text if caption > 1024 chars).

## Telegram setup

1. Create a bot via [@BotFather](https://t.me/BotFather), get the token.
2. Add the bot to your channel/group and grant admin rights (for channels) or make sure it can send messages.
3. Use the channel username (`@channelname`) or numeric chat ID.

## Safety

- The plugin never uploads the raw session transcript anywhere.
- Only the summary JSON and rendered image/PDF are used.
- Keep your Telegram bot token private.
