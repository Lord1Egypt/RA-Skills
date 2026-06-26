# OpenClaw Skills

A collection of useful skills for OpenClaw.

## Skills

### skill-linter

Analyze and validate SKILL.md files for best practices, common issues, and improvement suggestions.

**Usage:**
```bash
/skill-linter /path/to/SKILL.md
```

### duckduckgo-search

Search the web and fetch URL content using DuckDuckGo (no API key required).

**Prerequisites:**
```bash
pip3 install duckduckgo-search
```

**Usage:**
```bash
# Search
python3 duckduckgo-search/scripts/ddg_search.py "your query" --max-results 10

# Fetch URL
python3 duckduckgo-search/scripts/ddg_fetch.py "https://example.com"
```

## Installation

Install via ClawHub:

```bash
clawhub install skill-linter
clawhub install duckduckgo-search
```

## License

MIT
