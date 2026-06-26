# Supported URL Types

## URL Detection

| Source | Host Patterns | Extraction Method |
|--------|--------------|-------------------|
| 微信公众号 | `mp.weixin.qq.com`, `weixin.qq.com` | Jina Reader |
| Get 笔记 | `d.biji.com`, `biji.com` | Playwright |
| RSS / 播客 | `xiaoyuzhoufm.com`, any RSS | Direct HTTP |
| 公开网页 | `*` (all other URLs) | Jina Reader |

## Extraction Methods

### 1. Jina Reader (WeChat + General Pages)
```
GET https://r.jina.ai/<url>
Accept: application/json
```
Returns: `{"title": "...", "content": "..."}`

### 2. Playwright (Get 笔记)
```bash
node skills/anylink-to-note/scripts/getnote.js <url>
```
Returns: `{"title": "...", "content": "..."}`

### 3. RSS (Podcasts)
```bash
curl -sL "<rss-url>" | python3 -c "import sys,xmltodict; d=xmltodict.parse(sys.stdin.read()); print(d['rss']['channel']['item'][0]['description'])"
```

## Jina Reader Limitations

Jina Reader works for most public webpages but may fail for:
- Sites requiring login
- JS-rendered pages (Use Playwright instead)
- Sites blocking Jina's IP ranges

## Get 笔记 Notes

- Get 笔记 shared links use `d.biji.com/<id>` format
- Use Playwright to render and extract the full content
- Chromium must be installed: `npx playwright install chromium`
