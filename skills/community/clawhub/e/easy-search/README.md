# Easy Search Skill

A powerful web search skill that doesn't require API keys. It uses direct HTTP requests and the duckduckgo_search library for reliable results.

## Features

- **No API key required** - Uses public search interfaces
- **9 search engines** - Google, Bing, DuckDuckGo, Baidu, Sogou, 360, Brave, Yandex, Startpage
- **Auto engine selection** - Automatically picks the best available engine
- **Snippet extraction** - Get result previews, not just titles
- **Time filtering** - Filter by day/week/month/year
- **Interactive mode** - Continuous searching with live engine switching
- **Network diagnostics** - Built-in connectivity checking and proxy hints
- **Proxy support** - Respects ALL_PROXY, HTTPS_PROXY environment variables
- **Result caching** - Faster repeated searches
- **Smart failover** - Auto-switches to backup engines on failure

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/easy-search.git

# Optional: Install dependencies for better results
pip install duckduckgo-search requests
```

## Usage

### Basic Search

```bash
# Simple search
python3 scripts/search.py Python tutorial

# Specify engine
python3 scripts/search.py "AI news" --engine startpage

# More results
python3 scripts/search.py "React hooks" --results 10

# Markdown output
python3 scripts/search.py "machine learning" --format md
```

### Time Filtering

```bash
# News from last 24 hours
python3 scripts/search.py "AI news" --time day

# Results from last week
python3 scripts/search.py "React 19" --time week
```

### Interactive Mode

```bash
python3 scripts/search.py --interactive
```

### Network Diagnostics

```bash
python3 scripts/search.py --diagnose
```

## Search Engines

| Engine | Best For | Notes |
|--------|----------|-------|
| `auto` | General use | Auto-selects best available engine |
| `startpage` | Privacy, global | Privacy-focused, reliable parsing |
| `duckduckgo` | Privacy, global | Uses library if installed |
| `bing` | Global search | Good reliability |
| `google` | Best results | May need proxy |
| `baidu` | Chinese content | Strong anti-crawl |
| `sogou` | Chinese content | Alternative to Baidu |
| `brave` | Privacy-focused | Growing index |
| `yandex` | Russian/Global | Works in some regions |

## Proxy Configuration

```bash
export ALL_PROXY="http://127.0.0.1:7890"
python3 scripts/search.py "your query"
```

## License

MIT License