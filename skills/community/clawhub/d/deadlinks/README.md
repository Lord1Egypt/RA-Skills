# deadlinks 💀🔗

Fast broken link checker for Markdown files and websites. Zero dependencies, concurrent, CI-friendly.

## Features

- **Markdown-native** — understands `[text](url)` and `[ref]: url` syntax
- **Local + external** — checks both file references and HTTP links
- **Concurrent** — configurable thread pool (default 10 workers)
- **CI-friendly** — exits with code 1 if broken links found
- **Website crawling** — follow links to configurable depth
- **JSON output** — pipe results to other tools
- **Zero deps** — pure Python 3.10+, no pip install needed

## Usage

### Check Markdown files

```bash
# Single file
python3 deadlinks.py check README.md

# Directory (recursive, including external URLs)
python3 deadlinks.py check docs/ --recursive --external

# JSON output for CI
python3 deadlinks.py check . -r -e --format json
```

### Check a website

```bash
# Crawl and check all links on a page
python3 deadlinks.py url https://example.com

# Crawl 2 levels deep
python3 deadlinks.py url https://example.com --depth 2 --verbose
```

### Options

| Flag | Description |
|------|-------------|
| `--recursive, -r` | Recurse into subdirectories |
| `--external, -e` | Also check external HTTP(S) links |
| `--timeout, -t` | Request timeout in seconds (default: 10) |
| `--format, -f` | Output format: `text` or `json` |
| `--workers, -w` | Concurrent workers (default: 10) |
| `--verbose, -v` | Show progress |
| `--depth, -d` | Crawl depth for URL mode (default: 1) |

### Exit codes

- `0` — all links OK
- `1` — broken links found

## Examples

```
$ python3 deadlinks.py check docs/ -r -e
Checking 42 file(s)...
  ✗ docs/api.md:15 → https://old-api.example.com/v1 (HTTP 404)
  ✗ docs/guide.md:8 → ../missing-file.md (File not found)

============================================================
BROKEN LINKS (2)
============================================================
  docs/api.md:15
    → https://old-api.example.com/v1 [404]
  docs/guide.md:8
    → ../missing-file.md - File not found

Total: 156 | ✓ 152 | ✗ 2 | ⏱ 0 | ⚠ 0 | ⊘ 2
```

## Use in CI

```yaml
# GitHub Actions
- name: Check links
  run: python3 deadlinks.py check docs/ -r -e --timeout 15
```

## License

MIT
