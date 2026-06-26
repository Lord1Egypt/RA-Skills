---
name: broder-printer
description: Brother DCP-T426W network printer skill — IPP + driverless (primary), TCP direct (fallback for text-only, no sudo).
version: 5.0.0
---

# Brother DCP-T426W Printer Skill

## When to Use

- When you need to print text, images, or PDFs to a Brother DCP-T426W from a CLI or script
- When you're on a NAS, Linux, or macOS machine with CUPS and want driverless IPP printing
- When you need a text-only fallback on a headless or no-root system (TCP direct, no CUPS)
- When you want to check printer status or print a test page programmatically

## How It Works

Printing to a Brother DCP-T426W inkjet printer via two methods:

1. **IPP + driverless PPD (primary)** — Full support: text, images, PDFs. Requires CUPS with `driverless`.
2. **TCP direct (fallback)** — Text only, no CUPS, no sudo required.

**Supported platforms:** Any device with CUPS + `driverless` (NAS, Linux, macOS) or Python 3 with TCP access (fallback).

## Printer Info

| Field | Value |
|-------|-------|
| Model | Brother DCP-T426W |
| IP | 192.168.50.232 |
| Protocol | IPP (`ipp://192.168.50.232:631/ipp/print`) — primary; TCP 9100 fallback |
| Type | Color Inkjet MFP (Print / Scan / Copy) |
| Max Resolution | 4800 x 1200 dpi |
| Paper | A4, Letter, A5, A6, Photo (10x15cm), Envelopes |

## Quick Start

```bash
# Print a text string (CUPS IPP)
python scripts/print.py --text "Hello World"

# Print a file (text, image, PDF — CUPS handles conversion)
python scripts/print.py --file document.txt
python scripts/print.py --file photo.jpg
python scripts/print.py --file report.pdf

# Print a receipt-style text
python scripts/print.py --text "Invoice #123\nTotal: $42.00" --mode receipt

# Print a test page
python scripts/print.py --test

# Check printer status
python scripts/print.py --status

# Fallback: TCP direct (text only, no CUPS needed)
python scripts/print.py --text "Hello" --method tcp
```

## Architecture

```
broder-printer/
├── SKILL.md                    # This file
├── CLAUDE.md                   # Project documentation
├── Brother_DCP-T426W/          # Brother driver files (backup only)
│   ├── drivers/
│   │   ├── Brother_DCP-T426W.ppd
│   │   └── Brother DCP-T426W CUPS.gz
│   └── readme.md
├── requirements.txt
└── scripts/
    └── print.py                # Main print CLI (IPP/CUPS primary, TCP fallback)
```

## Setup (One-Time)

### Step 1: Install CUPS + driverless

```bash
# Linux (Debian/Ubuntu)
sudo apt install cups cups-filters ipp-usb
sudo systemctl enable --now cups

# macOS — CUPS is built-in, skip this step
```

### Step 2: Generate driverless PPD and add printer

```bash
# Generate PPD from printer's IPP capabilities
driverless "ipp://192.168.50.232:631/ipp/print" > ~/brother.ppd

# Add printer to CUPS
sudo lpadmin -p Brother_DCP-T426W \
  -v "ipp://192.168.50.232:631/ipp/print" \
  -E \
  -P ~/brother.ppd

sudo lpadmin -p Brother_DCP-T426W -o printer-is-shared=false

# Verify
lpstat -p Brother_DCP-T426W -l
```

### Step 3: Test

```bash
echo "Hello" | lp -d Brother_DCP-T426W
```

## How It Works

**IPP + driverless (default):**
1. Script calls CUPS `lp` command
2. CUPS converts input (text/image/PDF) to PWG-raster using the driverless PPD
3. Data sent to printer via IPP protocol
4. Printer renders and prints

**TCP direct (fallback, `--method tcp`):**
1. Script opens TCP socket to printer port 9100
2. Wraps text in PJL (Printer Job Language) commands
3. Sends data directly to printer
4. Text only — images/PDFs need CUPS conversion

## IPP vs TCP

| Feature | IPP + driverless | TCP Direct |
|---------|-----------------|------------|
| Setup | CUPS + `driverless` | None |
| sudo required | Setup only (once) | No |
| Text printing | Yes | Yes |
| Image printing | Yes (PWG-raster) | No (raw bytes only) |
| PDF printing | Yes | No |
| Print queue | Yes | No |
| Use case | NAS, desktop, full features | Headless, no-root, text-only |

## Direct CUPS Commands

```bash
# Print any file CUPS understands
lp -d Brother_DCP-T426W file.txt

# Print with options
lp -d Brother_DCP-T426W -o media=A4 -o sides=one-sided document.pdf

# Check jobs
lpstat -o Brother_DCP-T426W

# Cancel jobs
cancel Brother_DCP-T426W
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `driverless: command not found` | `sudo apt install cups-filters ipp-usb` |
| IPP connection refused | Verify printer supports IPP: `driverless` (list available IPP printers) |
| No paper output | Check paper tray, ink levels, printer not in error state |
| TCP prints garbled text | Printer may not support PJL PLAINTEXT — use IPP method |
| CUPS printer not found | `lpstat -p` to list printers; re-run lpadmin setup |
| `lp` command not found | `sudo apt install cups-client` |
