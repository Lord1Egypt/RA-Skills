---
name: deadlinks
description: Check Markdown files and websites for broken links. Use when asked to find dead links, validate URLs in docs, check if links still work, audit a README, or run a link health check. Zero dependencies.
---

# Deadlinks 💀🔗

Fast broken link checker for Markdown files and websites.

## Usage

```bash
# Check a Markdown file for broken links
python3 scripts/deadlinks.py check README.md

# Check with external URL validation
python3 scripts/deadlinks.py check README.md --external

# Check a directory recursively
python3 scripts/deadlinks.py check docs/ --recursive

# Check a website
python3 scripts/deadlinks.py check https://example.com
```

## Features
- Markdown link extraction (inline + reference)
- External URL validation (HTTP HEAD with fallback to GET)
- Concurrent checking (fast)
- CI-friendly exit codes (0 = all good, 1 = broken links found)
- Zero dependencies — pure Python
