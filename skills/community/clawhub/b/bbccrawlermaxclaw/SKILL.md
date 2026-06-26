# BBC Crawler MaxClaw

## Description
A powerful, universal web crawler optimized for BBC News but capable of crawling other sites. It integrates advanced scraping technologies including Crawl4AI and Playwright to handle dynamic content and anti-bot protections.

## Features
- **Multi-Method Extraction**: 
  - `crawl4ai`: Primary method using AsyncWebCrawler for high performance and accuracy.
  - `playwright`: Full browser rendering fallback for complex dynamic pages.
  - `requests`: Fast fallback for static content.
  - `auto`: Automatically detects the best method (Prioritizes Crawl4AI).
- **Hierarchical Storage**: Saves content in a structured format: `YYYY-MM-DD/Category/Title.md`.
- **Local Image Archiving**: Downloads images locally, names them by MD5 hash, and updates Markdown references.
- **Content Filtering**: Intelligently extracts main article content and relevant images using CSS selectors.

## Requirements
- Python 3.9+
- See `requirements.txt` for Python packages.

## Installation

```bash
# 1. Install dependencies
# Note: install.py supports passing arguments to pip, e.g., --break-system-packages
python install.py

# Example for environments requiring --break-system-packages:
python install.py --break-system-packages
```

## Usage

### Basic Usage
```bash
python universal_crawler_v2.py --url https://www.bbc.co.uk/news --max-pages 50
```

### Advanced Usage
```bash
# Force Crawl4AI
python universal_crawler_v2.py --url https://www.bbc.co.uk/news --method crawl4ai

# Force Playwright
python universal_crawler_v2.py --url https://www.bbc.co.uk/news --method playwright

# Control depth and delay
python universal_crawler_v2.py --url https://www.bbc.co.uk/news --depth 3 --delay 2.5

# Specify output directory
python universal_crawler_v2.py --url https://www.bbc.co.uk/news --output ./my_data
```

## Troubleshooting
- **Import Errors**: If you see "No module named 'crawl4ai'" or similar, run `python install.py` again.
- **Empty Responses**: Ensure you have the latest version of the crawler. Some sites may block specific IPs or user agents; try increasing delay or switching methods.
