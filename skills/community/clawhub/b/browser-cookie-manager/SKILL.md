---
name: browser-cookie-manager
version: 1.0.0
description: Read cookies from mainstream browsers and convert to specified format
whenToUse: When you need to quickly get cookies from browsers
---

## Overview

This skill reads cookies from 10 mainstream browsers for specified domains and converts them to multiple output formats.

## Supported Browsers

- Chrome (Windows/macOS/Linux)
- Edge (Windows/macOS/Linux)
- Firefox (Windows/macOS/Linux)
- Brave (Windows/macOS/Linux)
- Opera (Windows/macOS/Linux)
- OperaGX (macOS/Windows)
- Vivaldi (Windows/macOS/Linux)
- LibreWolf (Windows/macOS/Linux)
- Arc (macOS/Windows/Linux)
- Chromium (Windows/macOS/Linux)

## Usage

Run the script, select browser and domain, automatically read and output cookies.

## Output Format

- `json`: JSON format
- `cookie-header`: HTTP Cookie Header format
- `curl`: cURL command format

## Parameters

- `browser`: Browser name (required)
- `domain`: Target domain (required, e.g., douyin.com)
- `output_format`: Output format (optional, default json)
- `output_file`: Output file path (optional)

## Example

```bash
python scripts/read_cookie.py --browser chrome --domain douyin.com
python scripts/read_cookie.py --browser edge --domain tiktok.com --output-format cookie-header
python scripts/read_cookie.py --browser firefox --domain xiaohongshu.com --output-file cookies.json
```

## Tech Stack

- Python 3.11+
- rookiepy 0.5.6

## Notes

1. Windows system requires administrator privileges to read Chromium, Chrome, Edge browser cookies
2. Linux environment may be limited (headless)
3. Only for personal use, do not obtain others' cookies
4. Comply with browser privacy policy

## Legal Disclaimer

This skill is for learning and research purposes only.

Users must comply with the following principles when using this skill:
1. Not for any commercial use
2. Only for personal use, do not obtain others' cookies
3. Comply with browser privacy policy and platform terms of service
4. Do not use for any illegal or improper purposes

By using this skill, you agree to comply with the above principles.
