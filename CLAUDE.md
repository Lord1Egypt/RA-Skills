# Project Context: RA-Skills

This repository is a comprehensive registry of **90,896** Hermes-compatible AI agent skills.

## 📁 Key Files
- `registry.json`: Consolidated minified metadata index.
- `skills/built-in/`: 75 core skills with full prompts.
- `skills/optional/`: 95 extension skills with full prompts.
- `skills/community/`: Partitioned metadata markdown files for community registries.
- `tools/search.py`: Command-line tool for offline search.
- `tools/fetch_content.py`: Downloader to fetch community skill implementation on-demand.
- `tools/test_all.py`: Verification script to test all functions.

## 📐 Project Rules
1. **Name Truncation:** Subdirectories under `skills/community/` are truncated to a maximum of 80 characters to prevent path-length errors.
2. **Testing:** Always run `python3 tools/test_all.py` to ensure all query parameters and scraper functions are fully operational.
3. **No External Dependencies:** Keep `search.py` and `fetch_content.py` strictly based on Python's standard library.
