---
name: send-file
description: |
  Convert workspace files into Telegram-downloadable attachments (PDF/ZIP).
  Use when the user asks to receive, download, or be sent a file that was
  generated or exists in the workspace. Handles the OpenClaw MEDIA: delivery
  mechanism for Telegram channel.
allowed-tools:
  - Bash(mdpdf *)
  - Bash(zip *)
  - Bash(cp *)
  - Bash(ls *)
  - Bash(mkdir *)
---

# send-file

Convert local files into Telegram-friendly downloadable attachments.

## When to use

- User says "send me the file", "download", "attach", "share this"
- You generated a report, spreadsheet, or document the user wants
- Previous `MEDIA:` delivery of `.md` or raw text failed (user couldn't download)

## The Problem

OpenClaw's `MEDIA:` directive delivers files through Telegram's Bot API. However:
- **`.md` files** → Telegram shows inline as plain text, NOT as a downloadable document
- **`.zip` files** → Sometimes work, sometimes blocked
- **`.pdf` files** → ✅ Always delivered as a downloadable document
- **`.png/.jpg` files** → ✅ Always delivered as an image

## Solution

### Step 1: Convert to PDF

```bash
# Install if not already present
pip install --user --break-system-packages mdpdf 2>/dev/null

# Convert markdown → PDF
~/.local/bin/mdpdf -o /tmp/output.pdf /path/to/input.md
```

### Step 2: Deliver via MEDIA

In your reply, add:

```
MEDIA:/tmp/output.pdf
```

### For multiple files — ZIP them

```bash
cd /tmp && zip bundle.pdf.zip file1.pdf file2.pdf
```

Then:
```
MEDIA:/tmp/bundle.pdf.zip
```

**Important:** Name ZIP files with `.pdf.zip` suffix — Telegram handles these more reliably.

## Delivery Patterns

### Single markdown file
```bash
~/.local/bin/mdpdf -o /tmp/report.pdf /home/axiom/.openclaw/workspace/report.md
```
Reply:
```
MEDIA:/tmp/report.pdf
```

### Multiple markdown files
```bash
~/.local/bin/mdpdf -o /tmp/report1.md file1.md
~/.local/bin/mdpdf -o /tmp/report2.md file2.md
cd /tmp && zip reports.pdf.zip report1.pdf report2.pdf
```
Reply:
```
MEDIA:/tmp/reports.pdf.zip
```

### Already a binary file (PDF, image, etc.)
Just send directly — no conversion needed:
```
MEDIA:/path/to/file.pdf
```

### Non-markdown text files (CSV, JSON, etc.)
```bash
# Wrap in a zip for reliable download
cd /tmp && zip data.zip data.csv
```
Reply:
```
MEDIA:/tmp/data.zip
```

## OpenClaw MEDIA: Reference

The `MEDIA:/path` line in assistant output triggers OpenClaw's file delivery:
- Local paths are resolved against allowed roots: workspace, `/tmp`, `~/.openclaw/media/`
- Files are loaded and sent via the channel's native API (Telegram Bot API `sendDocument`)
- Must be on its own line, no other text on that line
- Multiple `MEDIA:` lines = multiple attachments

## Tool Dependencies

- **mdpdf** — Markdown to PDF converter (`pip install mdpdf`)
- **zip** — Standard Unix zip (usually pre-installed)
