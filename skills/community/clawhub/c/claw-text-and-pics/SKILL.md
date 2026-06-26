---
name: claw-text-and-pics
description: Extract text and embedded images from scanned documents, PDFs, and photos via Mistral OCR API. Use when reading receipts, invoices, contracts, handwritten notes, or any image or PDF containing text.
license: MIT
compatibility: Requires Mistral API key. Optional Pillow (pip install pillow) for image extraction. Python 3.11+.
metadata:
  author: photon78
  version: "1.0.0"
  env_required: MISTRAL_API_KEY
  env_optional: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
---

# claw-text-and-pics

**Extract text and images from documents via Mistral OCR**

Give your OpenClaw agent the ability to read scanned documents, PDFs, and images — extracting clean Markdown text and cropping out embedded images. Powered by [Mistral's OCR API](https://docs.mistral.ai/capabilities/document/).

## When to use
- Extract text from scanned documents, invoices, receipts, contracts
- Pull embedded images from PDFs or scans
- Convert handwritten notes or photos to searchable text
- Send extracted images directly to Telegram

## Usage

```bash
# Extract text only
python3 ocr.py --input scan.jpg

# Extract text from PDF (3 pages)
python3 ocr.py --input document.pdf --pages 3

# Extract embedded images
python3 ocr.py --input scan.jpg --extract-images --output-dir ./images/

# Extract images and send to Telegram
python3 ocr.py --input scan.jpg --extract-images --send --target 123456789

# Works with URLs too
python3 ocr.py --input https://example.com/document.pdf
```

## Output
- **stdout:** Extracted text as Markdown
- **Files:** Cropped images saved to `--output-dir` (only with `--extract-images`)

## Configuration

Set in `~/.openclaw/.env` or as environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `MISTRAL_API_KEY` | Yes | Your Mistral API key |
| `TELEGRAM_BOT_TOKEN` | Only for `--send` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Optional | Default chat ID (overridable with `--target`) |

## Environment Variables

```
MISTRAL_API_KEY=required        # Mistral API key — get one at console.mistral.ai
TELEGRAM_BOT_TOKEN=optional     # Required only when using --send
TELEGRAM_CHAT_ID=optional       # Default target chat ID (overridable with --target)
```

This skill reads `~/.openclaw/.env` as a fallback for credentials.
Ensure the file has restricted permissions: `chmod 600 ~/.openclaw/.env`

## Requirements
- Python 3.11+
- Mistral API key ([console.mistral.ai](https://console.mistral.ai))
- **Optional** (only for `--extract-images`): `pip install pillow`

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--input` | Yes | Local path or URL to image/PDF |
| `--extract-images` | No | Crop and save embedded images |
| `--output-dir` | No | Output directory (default: `./extracted-images`) |
| `--send` | No | Send extracted images via Telegram |
| `--target` | No | Telegram chat ID (or `TELEGRAM_CHAT_ID` env var) |
| `--pages` | No | Number of PDF pages to process |
| `--debug` | No | Print raw API response |
