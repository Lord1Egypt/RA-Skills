# chinese-ebook-downloader

An OpenClaw AgentSkill for downloading Chinese-language ebooks from multiple online sources.

## Features

- **Multi-source**: Primary (online book library, ~100% coverage), Secondary (another library), Fallback (Z-Library)
- **No daily limits**: Uses file hosting service which has no download quotas
- **Full automation**: Search → Decrypt → API → Download → Extract ZIP
- **GBK encoding support**: Properly handles Chinese filenames in ZIP archives
- **Batch download**: Resume-capable with progress tracking
- **Multiple formats**: PDF, EPUB, MOBI, AZW3

## Download Sources

| Source | Coverage | Daily Limit | Notes |
|--------|----------|-------------|-------|
| Source A (primary) | ~100% | None | Primary source |
| Source B (secondary) | ~8% | None | Fallback |
| Source C (Z-Library) | Medium | 10/day | Last resort |

## Installation

Install via [ClawHub](https://clawhub.com):
```bash
clawhub install chinese-ebook-downloader
```

Or clone from GitHub:
```bash
git clone https://github.com/yourusername/chinese-ebook-downloader.git
```

## Prerequisites

- Python 3.9+
- [Playwright](https://playwright.dev/): `pip install playwright && playwright install chromium`
- [OpenClaw](https://openclaw.ai) AgentSkill runtime (for SKILL.md to work as a skill)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SOURCE_A_BASE_URL` | *(built-in)* | Primary book source base URL |
| `SOURCE_B_BASE_URL` | *(built-in)* | Secondary book source base URL |
| `FILE_HOST_BASE_URL` | *(built-in)* | File hosting service base URL |
| `EBOOK_DEFAULT_PASSWORD` | *(built-in)* | Default file host password |

## Usage

### As an Agent Skill

Once installed, the skill auto-triggers when you ask to download a book:
> "下载《超越百岁》"
> "帮我找一下《癌症传》的电子版"
> "Download 《谷物大脑》 ebook"

### As Scripts

```bash
# Single book
python scripts/download_book.py --title "超越百岁" --author "彼得·阿提亚"

# Known file host URL
python scripts/download_book.py --file-url "<file_host_url>" --title "超越百岁"

# Batch download
python scripts/batch_download.py --book-list books.json --output-dir ~/Books/
```

### Batch Download JSON Format

```json
[
  {"title": "超越百岁", "file_url": "<file_host_url>", "password": "<password>"},
  {"title": "谷物大脑", "file_url": "<file_host_url>", "password": "<password>"}
]
```

## Workflow

```
Search primary source → Extract file host link → Browser decrypt
→ Wait countdown → JS API → curl download ZIP → Python extract (GBK)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `web_fetch` blocked | Use browser tool instead |
| Link 404 | Link expired, re-search |
| API returns non-200 | Re-navigate to file host, re-decrypt |
| Downloaded HTML not ZIP | Download URL expired, get fresh one |
| ZIP filenames garbled | Script handles this (cp437→gbk decode) |
| Slow downloads | Normal for free-tier file hosting |

## License

MIT
