---
id: cli-qr-refiner
name: CLI-QR-Refiner
version: 2.0.0
description: Professional utility to refine terminal-based ASCII QR code blocks (█, ▀, ▄) into high-definition PNG images.
metadata: { "openclaw": { "requires": { "bins": ["python3"] }, "emoji": "🔍" } }
---

# CLI-QR-Refiner

A specialized tool for OpenClaw agents to capture and refine rough ASCII/Unicode QR code blocks from CLI terminal outputs into crystal-clear, scannable PNG images.

## Features
- **Block Recognition**: Automatically interprets `█` (full), `▀` (upper), and `▄` (lower) block characters.
- **Pixel-Perfect Scaling**: Renders vector-like precision to ensure zero scanning failures.
- **Zero Dependencies**: Built on Python 3 + PIL (pre-installed on most systems).
- **Headless Optimized**: Designed specifically for server-side environments where terminal displays are unreliable.

## Dependencies
- **Runtime**: Python 3 (no external packages required — uses built-in PIL/Pillow)

## Tools & Commands
The refinement logic resides in `{baseDir}/scripts/cli_qr_refiner.py`.

### Refinement Command
```bash
python3 {baseDir}/scripts/cli_qr_refiner.py <input_txt_path> <output_png_path> [scale]
```

- `input_txt_path`: Path to text file containing ASCII QR code
- `output_png_path`: Path for output PNG image
- `scale` (optional): Pixel size per character cell, default 10

## Prompting / Behavior
### When to use
Trigger this skill when:
1. A CLI tool (e.g., WeChat, Aliyun, NPM) outputs a block-character matrix intended for scanning.
2. The user reports scanning failures due to terminal alignment, line-height, or font issues.

### How to use
1. **Capture**: Extract the raw character block from the terminal output.
2. **Save**: Write the captured block to a temporary file (e.g., `/tmp/qr_source.txt`).
3. **Refine**: Run the Python script to generate the high-def image.
4. **Deliver**: Send the refined PNG to the user.

## Examples
### Input (ASCII/Unicode)
```text
██████████████  ██  ██████████████
██          ██  ██  ██          ██
██  ██████  ██      ██  ██████  ██
```

### Output
A professional, high-definition PNG file, ready for any scanning app.

## How it works
Each character in the ASCII QR maps to a cell:
- `█` → full black cell
- `▀` → upper-half black cell
- `▄` → lower-half black cell
- ` ` (space) → white cell

The script scales each cell to `scale × scale*2` pixels for crisp rendering.
