# content-clipper

Extract, summarize, and clip web content to note-taking services. Use when: (1) user shares a URL and wants a summary or key points extracted, (2) user wants to save/clip content to flomo, local markdown, or other note services, (3) user says "剪藏", "摘录", "存到flomo", "记到笔记", "clip this", "save to flomo", (4) user shares a 小红书/微信公众号/Twitter link and wants content extracted. Supports: web articles, 小红书 notes (text + video via screenshot), Twitter/X posts. Outputs to: flomo (webhook), local markdown files.

## Usage

### Clip to flomo
```bash
node <skill_dir>/scripts/clip.js --url "https://example.com" --target flomo
```

### Clip to local markdown
```bash
node <skill_dir>/scripts/clip.js --url "https://example.com" --target markdown --output /path/to/file.md
```

### Options
- `--url` — URL to extract content from
- `--target` — Output target: `flomo` or `markdown` (default: flomo)
- `--output` — Output file path (for markdown target)
- `--summary` — Also generate a summary
- `--tags` — Comma-separated tags to add

## Flomo Configuration
Set webhook URL in the script or via environment variable `FLOMO_WEBHOOK`.
Default webhook (Candy): https://flomoapp.com/iwh/MTg4MTA/c6fceb66258d3cc5c527d82f283ba06a/

## Notes
- Windows: uses `curl.exe --noproxy '*'` for flomo webhook (proxy bypass needed)
- 小红书: extracts text content; video notes use screenshot fallback
- Twitter/X: extracts tweet text and media URLs
