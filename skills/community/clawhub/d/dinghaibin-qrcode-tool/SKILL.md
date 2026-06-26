---
name: qrcode-tool
description: Generate QR codes from text or URLs for easy sharing and scanning. Outputs as ASCII art or image files for printing and digital use.
---
# QR Code Generator

Create QR codes from text input, URLs, or contact information. QR codes can be scanned by mobile devices for quick access to links, text, or data.

## Usage
```bash
qrcode-tool [options] <data>
```

## Options

- `-o file`: Save QR code as image file (PNG)
- `-s N`: Set QR code size in pixels
- `-a`: Output as ASCII art in terminal

## Examples

```bash
qrcode-tool -a "https://example.com"
qrcode-tool -o qr.png "Hello World"
qrcode-tool -s 500 -o link.png "https://github.com"
```