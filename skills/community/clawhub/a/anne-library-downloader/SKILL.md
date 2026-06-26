# Anne's Library Downloader

Download books, articles, and DOIs from academic libraries with full automation.

## What This Skill Does

- Downloads PDFs from library databases
- Extracts DOIs from URLs
- Automates authentication for institutional access
- Handles VitalSource, ProQuest, EBSCO, and other academic platforms

## Installation

```bash
# Install dependencies
pip install playwright requests beautifulsoup4

# Install browser for Playwright
playwright install chromium
```

## Usage

```bash
# Download a book by title/author
anne-download --book "Essential Biological Psychology" --author "Martin, G. Neil"

# Download by DOI
anne-download --doi "10.1037/0000092-000"

# Download by URL
anne-download --url "https://library.capella.edu/..."

# Batch download from list
anne-download --list ~/Downloads/my_reading_list.txt
```

## Configuration

Set up library credentials:

```bash
# For Capella library
export ANNE_LIBRARY_URL="https://capella.alma.exlibrisgroup.com"
export ANNE_LIBRARY_USER="your_username"
export ANNE_LIBRARY_PASS="your_password"
```

## Supported Platforms

- VitalSource Bookshelf
- ProQuest
- EBSCOhost
- JSTOR
- PubMed Central
- ScienceDirect
- Springer Link
- Taylor & Francis Online

## Features

- **Auto-authentication**: Handles institutional login automatically
- **DOI extraction**: Pulls DOI from any academic URL
- **Metadata preservation**: Saves citation info alongside PDF
- **Batch processing**: Download entire reading lists
- **Format conversion**: Convert to PDF, EPUB, or text

## Files

- `scripts/download.py` — Main download script
- `scripts/auth.py` — Authentication handlers
- `scripts/doi_extractor.py` — DOI extraction
- `references/config.json` — Library configurations

---
*Skill created: March 8, 2026*