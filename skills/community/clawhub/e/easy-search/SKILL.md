---
name: "easy-search"
description: "Simple web search using multiple search engines with no API key required. Supports Google, Bing, DuckDuckGo, Baidu, Sogou, 360, Brave, Yandex. Features time filtering, interactive mode, snippet extraction, and network diagnostics."
---

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

## Requirements

- Python 3.6+
- Optional: `pip install duckduckgo-search requests` for better results

## Commands

### Basic Search

```bash
# Simple search (positional argument)
python3 {baseDir}/scripts/search.py Python tutorial

# With flag
python3 {baseDir}/scripts/search.py --query "your search terms"

# Specify engine
python3 {baseDir}/scripts/search.py "AI news" --engine bing

# More results
python3 {baseDir}/scripts/search.py "React hooks" --results 10

# JSON output (default)
python3 {baseDir}/scripts/search.py "Vue.js" --format json

# Markdown output
python3 {baseDir}/scripts/search.py "machine learning" --format md

# Simple output (quick reading)
python3 {baseDir}/scripts/search.py "Docker" --format simple

# CSV output
python3 {baseDir}/scripts/search.py "Kubernetes" --format csv
```

### Time Filtering

```bash
# News from last 24 hours
python3 {baseDir}/scripts/search.py "AI news" --time day

# Results from last week
python3 {baseDir}/scripts/search.py "React 19" --time week

# Results from last month
python3 {baseDir}/scripts/search.py "Python 3.13" --time month

# Results from last year
python3 {baseDir}/scripts/search.py "best laptops 2024" --time year
```

### Interactive Mode

```bash
# Start interactive mode
python3 {baseDir}/scripts/search.py --interactive

# In interactive mode:
# [auto]> Python tutorial          # Search with auto engine
# [auto]> :engine duckduckgo       # Change engine
# [duckduckgo]> React hooks        # Search with new engine
# [duckduckgo]> :format simple     # Change output format
# [duckduckgo]> :check             # Check engine health
# [duckduckgo]> :quit              # Exit
```

### Network Diagnostics

```bash
# Run network diagnostics
python3 {baseDir}/scripts/search.py --diagnose

# Check which engines are available
python3 {baseDir}/scripts/search.py --check-engines
```

### Engine Management

```bash
# Clear cache
python3 {baseDir}/scripts/search.py --clear-cache

# Disable auto-fallback (stay on specified engine)
python3 {baseDir}/scripts/search.py "query" --engine google --no-fallback
```

## Search Engines

| Engine | Best For | Notes |
|--------|----------|-------|
| `auto` | General use | Auto-selects best available engine |
| `startpage` | Privacy, global | Privacy-focused, reliable HTML parsing |
| `duckduckgo` | Privacy, global | Preferred, uses library if installed |
| `bing` | Global search | Good reliability, decent snippets |
| `google` | Best results | May need proxy in some regions |
| `baidu` | Chinese content | Strong anti-crawl measures |
| `sogou` | Chinese content | Good alternative to Baidu |
| `so360` | Chinese content | Another Chinese option |
| `brave` | Privacy-focused | Growing index |
| `yandex` | Russian/Global | Works in some regions |

## Output Formats

### JSON
```json
{
  "query": "search terms",
  "engine": "bing",
  "method": "HTML scraping",
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "snippet": "Brief description..."
    }
  ],
  "total": 5
}
```

### Markdown
```
## Search Results: your terms

Engine: **BING**
Method: _HTML scraping_

1. [Result Title](https://example.com)
   > Brief description...

2. [Another Title](https://another.com)
   > More info...
```

### Simple
```
1. Result Title
   https://example.com
   Brief description...

2. Another Title
   https://another.com
   More info...
```

## Examples

```bash
# Quick search for documentation
python3 {baseDir}/scripts/search.py "Python requests library docs"

# Search Chinese content with Sogou
python3 {baseDir}/scripts/search.py "人工智能最新进展" --engine sogou

# Get recent news in markdown format
python3 {baseDir}/scripts/search.py "OpenAI news" --time day --format md

# Use interactive mode for multiple searches
python3 {baseDir}/scripts/search.py -i

# Search with time filter
python3 {baseDir}/scripts/search.py "React 19 features" --time month --results 10
```

## Proxy Configuration

Set environment variables for proxy support:

```bash
# Set proxy
export ALL_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"

# Then run search
python3 {baseDir}/scripts/search.py "your query"
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Empty results | Try a different engine with `--engine` |
| Connection timeout | Check proxy settings or use `--timeout 60` |
| Rate limiting | Wait between searches or switch engines |
| DuckDuckGo slow | Install library: `pip install duckduckgo-search` |
| No snippets | Some engines have limited snippet extraction |
| Google blocked | Use proxy or switch to Bing/DuckDuckGo |
| All engines fail | Run `--diagnose` to check network |

## Tips for Best Results

1. **Use `auto` engine** - Let the tool pick the best available engine
2. **Install dependencies** - `pip install duckduckgo-search requests` for better reliability
3. **Use time filters** - For news and recent topics, use `--time day` or `--time week`
4. **Try Chinese engines** - Use `sogou` or `so360` for Chinese content
5. **Interactive mode** - Great for multiple related searches
6. **Cache is your friend** - Repeated searches are instant (1 hour cache)
7. **Run diagnostics** - Use `--diagnose` to troubleshoot network issues

## Version History

- **v1.1.0** - Added Startpage engine with proper parsing, fixed HTML entity decoding in URLs
- **v1.0.1** - Added network diagnostics, better proxy hints, improved error messages
- **v1.0.0** - Added 4 new engines (Sogou, 360, Brave, Yandex), time filtering, interactive mode, snippet extraction, engine health caching
- **v4.0.0** - Integrated duckduckgo_search library, auto engine selection
- **v1.0.0** - Initial release with basic search