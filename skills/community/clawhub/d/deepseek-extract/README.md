# DeepSeek Extract

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Extract full conversation content from DeepSeek shared chat links.

## What is DeepSeek Extract?

**DeepSeek Extract** is a skill that extracts complete conversation content from DeepSeek shared chat links (`chat.deepseek.com/share/...`). It uses Playwright (headless Chromium) to render the SPA page and extract structured conversation data.

## Features

- **Full conversation extraction** — Captures all user messages and AI responses
- **Multiple output formats** — Markdown (default) or JSON
- **Robust selectors** — Multiple CSS selector strategies with aggressive fallback
- **Error resilient** — Graceful handling of timeouts, anti-bot protection, and lazy loading
- **Debugging mode** — `--headed` flag for visual debugging when extraction fails

## Quick Start

### Prerequisites

```bash
pip install playwright
playwright install chromium
```

### Usage

```bash
# Basic extraction (outputs to ./deepseek_conversation.md)
python3 scripts/extract_deepseek.py "https://chat.deepseek.com/share/abc123"

# Specify output path and format
python3 scripts/extract_deepseek.py "https://chat.deepseek.com/share/abc123" \
  --output ./my_chat.json --format json

# Debug with headed browser
python3 scripts/extract_deepseek.py "https://chat.deepseek.com/share/abc123" --headed
```

### Command-line Options

| Option | Default | Description |
|--------|---------|-------------|
| `url` | (required) | DeepSeek share URL |
| `--output, -o` | `./deepseek_conversation.md` | Output file path |
| `--format, -f` | `markdown` | Output format: `markdown` or `json` |
| `--headed` | off | Run browser in headed mode for debugging |
| `--timeout` | `30000` | Page load timeout in milliseconds |

## Installation as a Skill

```bash
# Clone this repository
git clone https://github.com/zz0116/deepseek-extract.git

# Place in your skills directory
cp -r deepseek-extract ~/.openclaw/skills/
```

## How It Works

1. Launches headless Chromium via Playwright
2. Navigates to the DeepSeek share URL
3. Waits for JavaScript rendering to complete
4. Tries multiple CSS selector strategies to find message elements
5. Falls back to text-based parsing if CSS selectors fail
6. Outputs structured conversation data

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No messages extracted | Try `--headed` flag; DeepSeek may have anti-bot protection |
| Timeout error | Retry with `--timeout 60000` |
| `playwright` not found | Run `pip install playwright && playwright install chromium` |
| `python3` not found (Windows) | Use `python` instead |

## License

MIT License — see the [LICENSE.txt](LICENSE.txt) file for details.
