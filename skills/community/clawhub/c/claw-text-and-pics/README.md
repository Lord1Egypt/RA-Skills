# claw-text-and-pics

> Extract text **and** pictures from documents — for [OpenClaw](https://openclaw.ai) agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Give your OpenClaw agent the ability to read scanned documents, PDFs, and images. Powered by [Mistral's OCR API](https://docs.mistral.ai/capabilities/document/) — one of the most capable document OCR models available.

---

## What it does

```
Scan / PDF / Image  →  Mistral OCR  →  Markdown text + cropped images
                                              ↓ (optional)
                                       Telegram photo message
```

Your agent can hand it a scanned invoice, a handwritten note, or a multi-page PDF — and get back clean Markdown text. With `--extract-images`, embedded diagrams, photos, or charts are cropped out and saved as JPEG files.

---

## Requirements

- Python 3.11+
- Mistral API key ([console.mistral.ai](https://console.mistral.ai))
- **Optional** — only for `--extract-images`: `pip install pillow`
- **Optional** — only for `--send`: Telegram bot token

---

## Installation

```bash
git clone https://github.com/photon78/claw-text-and-pics.git
cd claw-text-and-pics

# Optional: image extraction support
pip install pillow
```

Export as environment variables (e.g. in your shell profile or OpenClaw env config):

```bash
export MISTRAL_API_KEY=your_key_here
export TELEGRAM_BOT_TOKEN=your_bot_token   # only needed for --send
export TELEGRAM_CHAT_ID=123456789          # optional default chat ID
```

OpenClaw users: set these in your agent's environment via `openclaw.json` or the OpenClaw plugin config.

---

## Usage

```bash
# Extract text from an image
python3 ocr.py --input scan.jpg

# Extract text from a PDF
python3 ocr.py --input document.pdf --pages 5

# Extract text from a URL
python3 ocr.py --input https://example.com/invoice.pdf

# Extract text + save embedded images
python3 ocr.py --input scan.jpg --extract-images --output-dir ./images/

# Extract images and send them to Telegram
python3 ocr.py --input scan.jpg --extract-images --send --target 123456789

# Debug: see raw Mistral API response
python3 ocr.py --input scan.jpg --debug
```

---

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--input` | Yes | Local path or URL to image or PDF |
| `--extract-images` | No | Crop and save embedded images (requires Pillow) |
| `--output-dir` | No | Where to save images (default: `./extracted-images`) |
| `--send` | No | Send extracted images to Telegram |
| `--target` | No | Telegram chat ID (or set `TELEGRAM_CHAT_ID`) |
| `--pages` | No | Number of pages to process (PDFs) |
| `--debug` | No | Print raw API response |

---

## Supported formats

| Format | Text extraction | Image extraction |
|--------|----------------|-----------------|
| JPEG / PNG | Yes | Yes |
| PDF | Yes | Yes |
| URL (image) | Yes | No (local file required for crop) |
| URL (PDF) | Yes | No (local file required for crop) |

---

## How image extraction works

Mistral OCR returns bounding-box coordinates for each embedded image. `claw-text-and-pics` uses those coordinates to crop the image directly from the original file using Pillow — so you always get a clean, valid JPEG regardless of what format Mistral returns internally.

---

## Using with OpenClaw

Add to your agent's `TOOLS.md`:

```
- **claw-text-and-pics** → `python3 /path/to/skills/claw-text-and-pics/ocr.py --input <file>`
  Extract text and images from scanned documents, PDFs, and images via Mistral OCR.
```

---

## FAQ

**Why doesn't image extraction work with URLs?**

Mistral returns bounding-box coordinates for embedded images, but the actual pixel data isn't included in the API response. To crop images, `claw-text-and-pics` needs access to the original file. With a URL input, the original file isn't available locally — so text extraction works fine, but `--extract-images` is skipped.

**Workaround:** Download the file first, then pass the local path:
```bash
wget https://example.com/document.pdf
python3 ocr.py --input document.pdf --extract-images --output-dir ./images/
```

**Does it work on Raspberry Pi (ARM64)?**

Yes — no native binaries required. Pure Python + Mistral API.

**Do I need Pillow for text extraction?**

No. Pillow is only needed when using `--extract-images`. Text-only extraction works with Python stdlib.

---

## Built with

- [Mistral OCR API](https://docs.mistral.ai/capabilities/document/) — document understanding
- [OpenClaw](https://openclaw.ai) — self-hosted AI agent platform
- [openclaw-docker-installer](https://github.com/photon78/openclaw-docker-installer) — production-ready OpenClaw setup

---

## License

MIT — see [LICENSE](LICENSE)
