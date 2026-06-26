# Obsidian Clipper

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that clips web content into your Obsidian Vault — with local media, tags, and cross-platform wikilinks.

Paste a URL, say "clip this" or "收藏", and get a well-formatted Obsidian note with downloaded images/videos.

## Supported Platforms

| Platform | API / Method | Media |
|---|---|---|
| X (Twitter) | fxtwitter API (no auth) | Images |
| WeChat 公众号 | mptext.top API | Images |
| Xiaohongshu 小红书 | SSR `__INITIAL_STATE__` parsing | Images, Video |
| Douyin 抖音 | [douyin-downloader](https://github.com/jiji262/douyin-downloader) | Video, Cover |
| GitHub | GitHub REST API | — |
| Web (generic) | defuddle → CDP → WebFetch | Images, Video |

## Install

Install from [ClawHub](https://clawhub.org):

```
/skill install @zgissing/obsidian-clipper
```

After installation, create a `config.yml` in the skill directory (`~/.claude/skills/obsidian-clipper/`):

```yaml
vault:
  base_path: "/path/to/your/Vault/Clippings"
```

Restart Claude Code and start clipping.

## Configuration

Copy `config.yml.example` to `config.yml` (setup.sh does this automatically). Only `vault.base_path` is required.

### Vault settings

```yaml
vault:
  base_path: ""                    # Required: absolute path to your clippings root
  attachments_dir: "attachments"   # Subdirectory for media files
  dirs:                            # Subdirectory names per platform
    x: "X"
    wechat: "WeChat"
    xiaohongshu: "小红书"
    douyin: "抖音"
    github: "GitHub"
    web: "Web"
```

### Douyin (optional)

Douyin requires the [douyin-downloader](https://github.com/jiji262/douyin-downloader) tool:

```bash
# 1. Clone the tool
git clone https://github.com/jiji262/douyin-downloader.git ~/tools/douyin-downloader

# 2. Install dependencies (Python 3.10+)
cd ~/tools/douyin-downloader
pip install -r requirements.txt

# 3. Get cookies
pip install playwright && python -m playwright install chromium
python -m tools.cookie_fetcher --config config.yml

# 4. Enable in config.yml
```

```yaml
douyin:
  enabled: true
  tool_path: "/path/to/douyin-downloader"
  python: "python3.11"
```

### Xiaohongshu proxy (optional)

If you need a proxy to access Xiaohongshu:

```yaml
xiaohongshu:
  proxy: "http://127.0.0.1:7890"
```

### CDP browser (optional)

For JS-rendered pages (SPAs), enable CDP:

```yaml
web:
  cdp_enabled: true
  cdp_url: "http://localhost:3456"
```

Requires Chrome with remote debugging enabled.

## Usage

In Claude Code, just paste a URL:

```
https://x.com/somebody/status/123456  收藏
```

```
https://mp.weixin.qq.com/s/xxxxx  存下来
```

```
https://github.com/user/repo  clip this
```

The skill auto-detects the platform and creates a note with:
- Frontmatter metadata (title, author, date, tags)
- Downloaded images/videos as local Obsidian embeds
- Auto-generated tags
- Cross-platform wikilinks (e.g., GitHub links in X articles create linked GitHub notes)

## Output Structure

```
{vault.base_path}/
├── attachments/          # All downloaded media
│   ├── article-title-1.jpg
│   ├── video-title.mp4
│   └── ...
├── X/                    # X/Twitter posts & articles
├── WeChat/               # WeChat 公众号 articles
├── 小红书/               # Xiaohongshu notes
├── 抖音/                 # Douyin videos
├── GitHub/               # GitHub repos
└── Web/                  # Everything else
```

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- `curl` (pre-installed on macOS/Linux)
- `python3` (for Xiaohongshu SSR parsing)
- `defuddle-cli` (optional, for Web handler): `npm install -g defuddle-cli`
- `douyin-downloader` (optional, for Douyin): see above
- Chrome with remote debugging (optional, for CDP fallback)

## License

MIT-0 (published on ClawHub)
