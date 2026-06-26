# Project Context: RA-Skills

This repository is a comprehensive registry of **90,896** Hermes-compatible AI agent skills.

## 📁 Key Files
- `registry.json`: Consolidated minified metadata index.
- `skills/built-in/`: 75 core skills with full prompts.
- `skills/optional/`: 95 extension skills with full prompts.
- `skills/community/`: **Full offline skill folders** (~88% downloaded) for community registries — real `SKILL.md` + bundled `scripts/`, `references/`, `skill-card.md`, `_meta.json`, assets. Path: `skills/community/<source>/<first_char>/<identifier>/`.
- `tools/search.py`: Command-line tool for offline search.
- `tools/bulk_download.py`: v3 bulk downloader of **full skill folders** (ClawHub ZIP + GitHub per-repo tree cache). Resumable via git-ignored `.ra_complete` markers. Env: `CLAWHUB_TOKEN`, `GITHUB_TOKEN`.
- `tools/fetch_content.py`: On-demand single-skill full-folder fetcher.
- `tools/test_all.py`: Verification script to test all functions.

## 📐 Project Rules
1. **Name Truncation:** Subdirectories under `skills/community/` are truncated to a maximum of 80 characters to prevent path-length errors.
2. **Testing:** Always run `python3 tools/test_all.py` to ensure all query parameters and scraper functions are fully operational.
3. **No External Dependencies:** Keep `search.py` and `fetch_content.py` strictly based on Python's standard library.
