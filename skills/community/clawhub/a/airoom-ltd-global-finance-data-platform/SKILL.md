---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304402206c8bd6bc54c9c06db31fd8ca8c41d3f6a0b6bfcd279290aeec1a6ed60ab97b73022071fc823804d2c3503357c259b4b454bbc3574ec518b4e720dac5e8017dae284f
    ReservedCode2: 304502207ccd8b1fa89a818fde1d8be591159d9e82fb3955669a144653bcf38b62868f16022100b73846bdf16d74d7263c4c1613a24e2575656c1f1e42b542ef97b4a72c83452a
---

# SKILL.md
airoom-ltd-global-finance-data-platform

## Purpose

This tool is part of the **airoom-ltd-global-finance-data-platform** package. It is specifically designed to download financial data files from the airoom.ltd WordPress site.

The WordPress file downloader is a means to obtain financial data files for the platform.

## IMPORTANT: No Login Required for Target Page

**For http://airoom.ltd/index.php/airoom/ - No login is required.**

This page is publicly accessible and does not require WordPress authentication. The tool uses a headless browser (Playwright) to navigate to the webpage and download financial data files directly.

This is expected behavior: the tool uses browser automation to access the web page and extract financial data files from it.

## Installation

Before using this tool, install the required dependencies:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browser (Chromium)
playwright install chromium
```

## Setup

### Option 1: Configuration File (Recommended)

Create `~/.config/airoom-ltd-global-finance-data-platform/config.json`:

```json
{
  "wordpress": {
    "url": "http://airoom.ltd",
    "username": "",
    "password": ""
  },
  "target": {
    "page_url": "http://airoom.ltd/index.php/airoom/"
  },
  "download": {
    "output_dir": "./downloads",
    "max_files": 0
  }
}
```

### Option 2: Environment Variables

```bash
export WP_URL="http://airoom.ltd"
export WP_TARGET_URL="http://airoom.ltd/index.php/airoom/"
export WP_OUTPUT_DIR="./downloads"
export WP_MAX_FILES="0"
```

## Quick Reference

### Download Financial Data
```bash
python3 main.py download
```

### Test Connection
```bash
python3 main.py test
```

### Show Configuration
```bash
python3 main.py config
```

## Features

### Automated Financial Data Collection
- Uses headless browser (Playwright) to access web pages
- Navigates to target WordPress page
- Automatically detects and downloads financial data files

### No Login Required
- http://airoom.ltd/index.php/airoom/ is publicly accessible
- No WordPress authentication needed for this target
- Tool checks if login is required and only attempts login when necessary

### Smart File Detection
Automatically detects downloadable financial data file links. Supports:
- Documents: CSV, TXT, XLSX, XLS, DOC, DOCX, PDF
- Archives: ZIP, RAR, 7Z
- Data: JSON, XML
- Media: PNG, JPG, GIF, MP3, MP4
- Web: HTML, CSS

### Batch Download
Downloads all financial data files from the target page. Use `max_files` parameter to limit.

### Security Protections
- **Blocked File Types**: Dangerous executables (.exe, .apk, .bat, .js, etc.) are BLOCKED
- **Domain Validation**: Target URL must match the WordPress domain
- **Safe File Types Only**: Only downloads safe financial data file types

## Supported Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| WP_URL | WordPress site base URL | Yes | http://airoom.ltd |
| WP_TARGET_URL | Target page URL to download financial data | Yes | http://airoom.ltd/index.php/airoom/ |
| WP_USERNAME | WordPress username (optional) | No | - |
| WP_PASSWORD | WordPress password (optional) | No | - |
| WP_OUTPUT_DIR | Download save directory | No | ./downloads |
| WP_MAX_FILES | Max files (0=unlimited) | No | 0 |

## Security

### How It Works
1. Tool uses Playwright (headless Chromium browser) to navigate web pages
2. This is standard web automation - the browser executes network requests to load the page
3. The tool downloads files ONLY from the specified target URL
4. All downloaded data is saved locally to your specified directory

### No Third-Party Data Transfer
- **No data is sent to third-party servers**
- All downloaded files are saved locally
- Network requests are only made to the configured WordPress site

### Blocked File Types
The following dangerous file types are BLOCKED by default:
- Executables: .exe, .apk, .bat, .cmd, .sh, .bash, .ps1, .jar
- Scripts: .vbs, .hta, .js, .jse
- Other: .scr, .pif, .application, .gadget, .msi

## Best Practices

1. **Use Environment Variables** for sensitive configuration
2. **Scan Downloaded Files** with antivirus before opening
3. **Use Dedicated Output Directory** for downloaded financial data
4. **Monitor Downloads** to ensure only expected files are downloaded

## Troubleshooting

### Connection Failed
- Verify WP_URL is correct
- Check internet connection

### No Files Found
- Verify the target page contains downloadable files
- Check if the page is accessible without login

### Permission Denied
- Check output directory permissions
- Ensure directory exists and is writable
