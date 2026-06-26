---
name: obsidian-clipper
description: "Universal web clipper for Obsidian Vault. Saves content from X/Twitter, WeChat, Douyin, Xiaohongshu, GitHub, and generic web pages. Triggers when user sends a URL and asks to save/clip/收藏, or says '存下来'."
---

# Obsidian Clipper

Universal clipper — saves URLs from any platform to your Obsidian Vault with local media, tags, and wikilinks.

## Configuration

On first run, read `config.yml` from **the same directory as this SKILL.md file**. If missing, tell the user to copy `config.yml.example` to `config.yml` and fill in `vault.base_path`.

Key paths derived from config:

```
BASE        = config.vault.base_path
ATTACHMENTS = BASE / config.vault.attachments_dir
X_DIR       = BASE / config.vault.dirs.x
WECHAT_DIR  = BASE / config.vault.dirs.wechat
XHS_DIR     = BASE / config.vault.dirs.xiaohongshu
DOUYIN_DIR  = BASE / config.vault.dirs.douyin
GITHUB_DIR  = BASE / config.vault.dirs.github
WEB_DIR     = BASE / config.vault.dirs.web
```

---

## URL Router

Match the URL and dispatch to the correct handler:

| URL pattern | Handler |
|---|---|
| `x.com/*` or `twitter.com/*` | X Handler |
| `mp.weixin.qq.com/*` | WeChat Handler |
| `xhslink.com/*` or `xiaohongshu.com/*` | Xiaohongshu Handler |
| `v.douyin.com/*` or `douyin.com/video/*` | Douyin Handler |
| `github.com/{owner}/{repo}` (no deeper path) | GitHub Handler |
| Everything else | Web Handler |

---

## Shared Rules

These apply to ALL handlers:

### File naming
- Use the content title as filename
- Strip `/\:*?"<>|` and all emoji / special Unicode
- Truncate if >60 characters
- If a file with the same name exists, ask the user before overwriting

### Tags
- Every clipping MUST have the `clipping` tag
- No `.` or spaces in tags (`llms.txt` → `llms-txt`, `Claude Code` → `Claude-Code`)
- Add 2-4 content-based tags automatically

### Media download
- Download all images and videos to `ATTACHMENTS/`
- Image naming: `{title-slug}-{n}.{ext}` (slug ≤20 chars, no emoji)
- Video naming: `{title-slug}.mp4` or `{title-slug}-video-{n}.mp4`
- Replace remote URLs with Obsidian wikilinks: `![[filename.ext]]`

### "Why clipped" field
- Infer from conversation context if possible
- If context is insufficient, ask the user

### Cross-platform linking
- If the content contains a `github.com/{owner}/{repo}` link, auto-trigger the GitHub Handler to create a GitHub note, then add bidirectional wikilinks

---

## X Handler

Saves X (Twitter) posts and articles.

### Step 1: Fetch post data

```bash
curl -s "https://api.fxtwitter.com/{handle}/status/{tweet_id}"
```

Extract from URL: `x.com/{handle}/status/{id}` → handle, tweet_id.

Fields:
- `tweet.author.name` → author name
- `tweet.author.screen_name` → @handle
- `tweet.text` → post body (short posts)
- `tweet.article` → long-form article (if present)
- `tweet.article.title` → article title
- `tweet.article.content.blocks` → structured content (Draft.js format)
- `tweet.created_at` → publish date
- `tweet.likes` / `tweet.retweets` / `tweet.views` → engagement
- `tweet.media` → short post images
- `tweet.article.media_entities` → article inline images

### Step 2: Determine content type

**Short post** (`tweet.article` is null): use `tweet.text`, images from `tweet.media.photos`.

**Article** (`tweet.article` exists): parse `tweet.article.content.blocks` (Draft.js):

| block type | Markdown |
|---|---|
| `unstyled` | paragraph |
| `header-one` | `# heading` |
| `header-two` | `## heading` |
| `header-three` | `### heading` |
| `unordered-list-item` | `- item` |
| `ordered-list-item` | `1. item` |
| `atomic` | insert image `![[filename]]` |
| `blockquote` | `> quote` |

Inline styles: `Bold` → `**text**`, `Italic` → `*text*`.

For `atomic` blocks: `entityMap` → `value.data.mediaItems[].mediaId` → match `media_entities` → `media_info.original_img_url`.

### Step 3: Download images

Download all images to `ATTACHMENTS/`.

### Step 4: Generate file

Write to `X_DIR/{title}.md`:

**Short post:**
```markdown
---
title: "{author name}的推文 - {first 30 chars}"
author: "{author name}"
handle: "@{screen_name}"
source: {original URL}
date: {publish date YYYY-MM-DD}
tags:
  - clipping
  - {auto tags}
---

# {author name}的推文

> X: @{handle} ({name}) | {date} | {likes} likes · {retweets} retweets · {views} views

{body text}

{images ![[filename]]}
```

**Article:**
```markdown
---
title: "{article.title}"
author: "{author name}"
handle: "@{screen_name}"
source: {original URL}
date: {publish date YYYY-MM-DD}
tags:
  - clipping
  - {auto tags}
---

# {article.title}

> X: @{handle} ({name}) | {date} | {likes} likes · {retweets} retweets · {views} views

{parsed Markdown body with ![[local images]]}
```

### Notes
- fxtwitter API needs no auth but may rate-limit; try `vxtwitter.com` as fallback
- Title: articles use `article.title`; short posts use `{name}-{first 15 chars of text}`

---

## WeChat Handler

Saves WeChat Official Account (公众号) articles.

### Step 1: Fetch article data

```bash
curl -s "https://down.mptext.top/api/public/v1/download?url={URL-encoded-link}&format=json"
```

Extract: `title`, `nick_name`, `create_time`, `content_noencode`, `link`.

If API returns 204 or fails, fall back to `defuddle` or `WebFetch`.

### Step 2: Fetch HTML (if rich content needed)

If content has images or complex formatting:

```bash
curl -s "https://down.mptext.top/api/public/v1/download?url={URL-encoded-link}&format=html"
```

Extract image URLs and formatted content from HTML.

### Step 3: Download images

- Download each image to `ATTACHMENTS/`
- WeChat image URLs: `mmbiz.qpic.cn/mmbiz_png/...` → `.png`, `mmbiz_jpg/...` → `.jpg`
- Replace with `![[filename.jpg]]`

### Step 4: Generate file

Write to `WECHAT_DIR/{title}.md`:

```markdown
---
title: "{article title}"
author: "{公众号 name}"
source: {original link}
date: {publish date YYYY-MM-DD}
tags:
  - clipping
  - {auto tags}
---

# {article title}

> 公众号：{name} | {publish date}

{body with ![[local images]]}
```

---

## Xiaohongshu Handler

Saves 小红书 notes (images + video).

### Step 1: Resolve short link

If URL is `xhslink.com`, follow redirects to get the real URL **with full query parameters** (especially `xsec_token`):

```bash
curl -sL "<short-link>" -o /dev/null -w "%{url_effective}"
```

> **Important**: The full query string is required. Bare URLs return empty `noteDetailMap`.

### Step 2: Fetch SSR data

Xiaohongshu is an SPA, but SSR embeds data in `window.__INITIAL_STATE__`:

```bash
curl -sL "<full-URL-with-params>" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Accept: text/html" | python3 -c "
import sys, re, json

html = sys.stdin.read()
m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*</script>', html, re.DOTALL)
if not m:
    print('NO_DATA')
    sys.exit(1)

raw = m.group(1).replace(':undefined', ':null')
d = json.loads(raw)

note_map = d.get('note', {}).get('noteDetailMap', {})
for nid, detail in note_map.items():
    n = detail.get('note', {})
    result = {
        'title': n.get('title', ''),
        'desc': n.get('desc', ''),
        'type': n.get('type', ''),
        'author': n.get('user', {}).get('nickname', ''),
        'time': n.get('time', ''),
        'images': [],
        'video_url': None,
        'tags': [t.get('name', '') for t in n.get('tagList', [])]
    }
    for img in n.get('imageList', []):
        url = img.get('urlDefault', '') or img.get('urlPre', '') or img.get('url', '')
        if url: result['images'].append(url)
    video = n.get('video', {})
    if video:
        media = video.get('media', {})
        stream = media.get('stream', {})
        for codec in ['h264', 'h265', 'h266', 'av1']:
            streams = stream.get(codec, [])
            if streams:
                result['video_url'] = streams[0].get('masterUrl', '')
                break
    print(json.dumps(result, ensure_ascii=False))
"
```

### Step 3: Download media

- Images: `curl -L -o` each image to `ATTACHMENTS/`
- Video (if present): `curl -L -o` to `ATTACHMENTS/{title-slug}-video.mp4`

### Step 4: Generate file

Write to `XHS_DIR/{title}.md`:

```markdown
---
title: "{title}"
author: "{author}"
source: {real URL}
domain: xiaohongshu.com
date: {today YYYY-MM-DD}
tags:
  - clipping
  - {tags from tagList, 2-4}
---

# {title}

> 来源：小红书 | {author} | {publish date}

![[cover-image.jpg]]

![[video.mp4]]  (if video exists)

{desc body, strip [话题]# markers}

## 标签

{tags joined with /}
```

### Notes
- If curl can't reach Xiaohongshu, add `--proxy {config.xiaohongshu.proxy}`
- `desc` often contains `[话题]#tag[话题]#` markers — strip them for clean text

---

## Douyin Handler

Saves 抖音 videos. **Requires douyin-downloader tool** — check `config.douyin.enabled` first. If disabled, tell the user to install douyin-downloader and enable it in config.

### Step 1: Extract and resolve link

From share text like `7.94 复制打开抖音...https://v.douyin.com/xxxxx/ DUL:/...`, extract the `v.douyin.com` short link.

Resolve to full video ID:

```bash
curl -sI -L --max-redirs 5 "https://v.douyin.com/xxxxx/" 2>&1 | grep -i location | grep '/video/' | sed 's|.*/video/\([0-9]*\).*|\1|' | head -1
```

Construct: `https://www.douyin.com/video/{aweme_id}`

### Step 2: Download with douyin-downloader

1. Edit `{config.douyin.tool_path}/config.yml`: set `link` to the full URL
2. Run:
   ```bash
   cd {config.douyin.tool_path} && {config.douyin.python} run.py
   ```
3. Find files in `Downloaded/` — `.mp4`, `_cover.jpg`, `_data.json`

### Step 3: Extract metadata

From `_data.json`:
- `desc` → description (title + hashtags)
- `author.nickname` → author
- `statistics.digg_count` → likes
- `statistics.comment_count` → comments
- `statistics.share_count` → shares
- `create_time` → Unix timestamp → convert to YYYY-MM-DD

### Step 4: Copy media to vault

Copy video and cover to `ATTACHMENTS/`.

### Step 5: Generate file

Write to `DOUYIN_DIR/{title}.md`:

```markdown
---
title: "{video title}"
source: https://www.douyin.com/video/{aweme_id}
author: "{author}"
platform: 抖音
digg: {likes}
comment: {comments}
share: {shares}
created: {publish date YYYY-MM-DD}
date: {today YYYY-MM-DD}
tags:
  - clipping
  - 抖音
  - {auto tags}
---

# {video title}

> {original desc with hashtags}

## 为什么收藏

{inferred or asked}

## 视频

![[{video-file}.mp4]]

## 封面

![[{cover-file}_cover.jpg]]
```

### Notes
- Short links MUST be resolved first — douyin-downloader cannot handle them
- If download fails (0% success), cookies may be expired — tell user to re-run cookie fetcher:
  ```bash
  cd {config.douyin.tool_path} && {config.douyin.python} -m tools.cookie_fetcher --config config.yml
  ```
- `create_time` is Unix timestamp: `python3 -c "import datetime; print(datetime.datetime.fromtimestamp({ts}).strftime('%Y-%m-%d'))"`

---

## GitHub Handler

Saves GitHub repositories.

### Step 1: Fetch repo metadata

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}"
```

Extract: `name`, `full_name`, `description`, `stargazers_count`, `language`, `license.spdx_id`, `topics`, `created_at`, `html_url`, `homepage`.

### Step 2: Fetch README

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/readme"
```

Decode base64 `content` to get README markdown.

### Step 3: Summarize README

Do NOT copy the full README. Extract:
1. **Core features**: 3-5 bullet points, one sentence each
2. **Quick start**: only the most essential command or API snippet
3. **Notes**: limitations, dependencies, special requirements

### Step 4: Generate file

Write to `GITHUB_DIR/{repo-name}.md`:

```markdown
---
title: "{repo name}"
source: {repo URL}
author: "{owner}"
stars: {star count}
language: "{primary language}"
license: "{license}"
created: {repo created date YYYY-MM-DD}
date: {today YYYY-MM-DD}
tags:
  - clipping
  - github
  - {auto tags from topics}
---

# {repo name}

> {one-line description}

## 为什么收藏

{inferred or asked}

## 核心功能

- {point 1}
- {point 2}
- ...

## 快速开始

{minimal code block}

## 备注

{limitations, dependencies, notes}
```

### Notes
- Star count as raw number (no `1.2k` formatting — for Dataview sorting)
- Use `name` not `full_name` for filename
- If API returns 403 (rate limit), tell user to wait
- Strip emoji from filenames

---

## Web Handler

Saves generic web pages. Fallback for URLs that don't match any platform handler.

### Step 1: Extract content with defuddle

```bash
defuddle parse <url> --json
```

Extract: `title`, `author`, `content` (HTML), `description`, `published`, `domain`.

If defuddle is not installed, run `npm install -g defuddle-cli` first.

### Step 2: Handle empty content (SPA fallback)

If `content` is empty or just `<body></body>` (client-rendered SPA), try fallback paths in order:

**Path A: CDP browser** (if `config.web.cdp_enabled`):

1. Open page: `curl -s "{config.web.cdp_url}/new?url=<URL>"` → get `targetId`
2. Scroll: `curl -s "{cdp_url}/scroll?target=<ID>&direction=bottom"`
3. Extract title: `curl -s -X POST "{cdp_url}/eval?target=<ID>" -d 'document.title'`
4. Extract body: `curl -s -X POST "{cdp_url}/eval?target=<ID>" -d "document.querySelector('article')?.innerHTML || document.querySelector('main')?.innerHTML || document.body.innerHTML"`
5. Extract images: `curl -s -X POST "{cdp_url}/eval?target=<ID>" -d "[...document.querySelectorAll('img')].map(i=>i.src).filter(s=>s.startsWith('http'))"`
6. Extract videos: `curl -s -X POST "{cdp_url}/eval?target=<ID>" -d "[...document.querySelectorAll('video source, video')].map(v=>v.src||v.querySelector('source')?.src).filter(Boolean)"`
7. Close tab: `curl -s "{cdp_url}/close?target=<ID>"`

**Path B: WebFetch** — use the `WebFetch` tool as fallback.

**Path C: Bookmark mode** — if URL is a web app/tool/dashboard or all paths fail, create a bookmark note from meta info only.

### Step 3: Download media

Download images and videos to `ATTACHMENTS/`, replace with `![[filename]]`.

### Step 4: Generate file

Write to `WEB_DIR/{title}.md`:

**Content page:**
```markdown
---
title: "{page title}"
author: "{author}"
source: {URL}
domain: "{domain}"
date: {today YYYY-MM-DD}
tags:
  - clipping
  - {auto tags}
---

# {page title}

> 来源：{domain} | {author} | {publish date}

{Markdown body with ![[local media]]}
```

**Bookmark page** (tool/app/SPA):
```markdown
---
title: "{page title}"
author: "{author}"
source: {URL}
domain: "{domain}"
date: {today YYYY-MM-DD}
tags:
  - clipping
  - {auto tags}
---

# {page title}

> 来源：{domain} | {URL}

{description}

## 为什么收藏

{inferred or asked}

## 核心功能

- {points from meta info}
```

### Notes
- defuddle does not work on SPAs (React/Vue client-rendered) — use CDP path
- Always close CDP tabs after use
