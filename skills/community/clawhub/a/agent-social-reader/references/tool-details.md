# Platform Tool Details

When the Routing Map in SKILL.md routes to a specific tool, read this file for the exact commands, API parameters, and error handling.

## Service Boundaries

Only call a service when the current user request requires that service. Do not send the same content to every listed service.

- AgentLens receives a URL only when AgentLens is needed for the current read request.
- OpenAI Whisper receives audio only if the user chooses API transcription.
- Notion and ima receive archive content only when the user asks to save the current item and confirms the target destination.
- Obsidian writes to the user's local vault path.
- Credential examples read only the explicit variables and config paths shown here. Prefer platform secret storage or environment variables; use local plaintext files only after user approval.

---

## 1. General Web Pages — r.jina.ai

**Tool**: r.jina.ai
**API key**: None (free)
**Command**:
```bash
curl -L -s "https://r.jina.ai/{url}"
```
Returns clean Markdown. Works for most public web pages.

**Note**: `{url}` must include the full `https://` prefix:
```bash
curl -L -s "https://r.jina.ai/https://example.com/article"
```

**Fallback**: If Jina returns empty content, the page likely requires JS rendering. Try Camoufox or AgentLens.

---

## 2. X / Twitter — FxTwitter API

**Tool**: FxTwitter API
**API key**: None (free, no login or cookie required)
**Code**:
```python
import urllib.request, urllib.error, re, json

def fetch_tweet(url):
    pattern = r'(?:x\.com|twitter\.com)/([a-zA-Z0-9_]{1,15})/status/(\d+)'
    match = re.search(pattern, url)
    if not match:
        return {"error": f"Cannot parse tweet URL: {url}"}
    username, tweet_id = match.group(1), match.group(2)
    api_url = f"https://api.fxtwitter.com/{username}/status/{tweet_id}"
    req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"FxTwitter HTTP {e.code}: could not fetch tweet (may be deleted or private)"}
    except Exception as e:
        return {"error": f"FxTwitter error: {e}"}
    if data.get("code") != 200:
        return {"error": f"FxTwitter error: {data.get('message')}"}
    tweet = data["tweet"]
    return {
        "text": tweet.get("text", ""),
        "author": tweet.get("author", {}).get("name", ""),
        "screen_name": tweet.get("author", {}).get("screen_name", ""),
        "likes": tweet.get("likes", 0),
        "retweets": tweet.get("retweets", 0),
        "views": tweet.get("views", 0),
        "replies": tweet.get("replies", 0),
        "created_at": tweet.get("created_at", ""),
        "media": tweet.get("media", {}).get("all", []),
        "quote": tweet.get("quote", {})
    }
```
**Fallback**: AgentLens API (use when FxTwitter returns NOT_FOUND or rate-limit error)
**Limitation**: Thread replies, user timelines, X Lists, and private accounts are not supported by any free tool. AgentLens does not support these either.

---

## 3. YouTube — youtube-transcript-api

**Tool**: youtube-transcript-api
**API key**: None (free)
**Installation**: `pip install youtube-transcript-api`
**Code**:
```python
import re

def get_youtube_subtitle(video_url, lang="en"):
    from youtube_transcript_api import YouTubeTranscriptApi
    patterns = [
        r'(?:youtube\.com/watch\?.*?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
    ]
    video_id = None
    for pat in patterns:
        m = re.search(pat, video_url)
        if m:
            video_id = m.group(1)
            break
    if not video_id:
        return {"error": "Cannot parse YouTube URL"}
    # Language priority: requested lang first, then zh-Hans/zh/en, then any available
    langs = [lang, "zh-Hans", "zh", "en"]
    try:
        # Try 0.x API
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
        entries = [
            {"text": entry["text"], "start": entry["start"], "duration": entry["duration"]}
            for entry in transcript_list
        ]
        text = " ".join(e["text"] for e in entries)
        return {"video_id": video_id, "language": lang, "transcript": text, "entries": entries}
    except Exception:
        pass
    # Fallback to 1.x API
    try:
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=langs)
        entries = [
            {"text": s.text, "start": s.start, "duration": s.duration}
            for s in fetched
        ]
        text = " ".join(e["text"] for e in entries)
        return {"video_id": video_id, "language": lang, "transcript": text, "entries": entries}
    except Exception as e:
        return {"error": f"YouTube transcript unavailable: {e}. Try video summarization via SOP C."}
```
**Transcript source priority**: Creator-uploaded subtitles → auto-generated subtitles.
**Fallback**: If blocked (403/429 from YouTube), fall back to AgentLens API + Whisper (see SOP C).
**Limitation**: Subtitles must be enabled on the video. If fully disabled, use SOP C.

---

## 4. WeChat Official Account — Camoufox

**Tool**: Camoufox (headless browser for JS-rendered content)
**API key**: None (free)
**Installation**: `pip install camoufox`
**Compatibility note**: Camoufox may download a large browser bundle on first launch and can fail with Playwright protocol errors on some Python/browser-version combinations. Treat Camoufox as a best-effort renderer, not a guaranteed dependency.
**Code**:
```python
import asyncio
from camoufox.async_api import AsyncCamoufox

async def read_wechat(url):
    async with AsyncCamoufox(headless=True) as browser:
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)
            content = await page.locator("body").inner_text()
            return content
        finally:
            await page.close()

print(asyncio.run(read_wechat("https://mp.weixin.qq.com/s/ARTICLE_ID"))[:5000])
```
**Fallback**: If Camoufox fails or is unavailable, try AgentLens API if configured. If all automated paths fail, ask the user to share copied text or screenshots.

---

## 5. Weibo — r.jina.ai

**Tool**: r.jina.ai
**API key**: None (free)
**Command**:
```bash
curl -L -s "https://r.jina.ai/{weibo_url}"
```
r.jina.ai handles Weibo's mobile pages and bypasses login walls in most cases.
**Fallback**: AgentLens API.

---

## 6. AgentLens API — 20+ Social Platforms

**Purpose**: Mandatory handling channel for all platforms not covered by free tools above.
**Primary endpoint**: `POST https://agentlensapi.io/api/v1/fetch`
**Avoid by default**: `https://api.agentlensapi.io/v1/fetch` because some local proxy/fake-IP environments can fail TLS for the API subdomain while the main host works.
**Auth**: `Authorization: Bearer {AGENT_LENS_API_KEY}`

**Boundary**: Send only the URL for the current read request. Do not include unrelated user files, saved archives, or credentials in the request body.

#### Supported Platforms

| Global Platforms | Chinese Platforms |
|:---|:---|
| TikTok | Douyin |
| Instagram | Xiaohongshu |
| YouTube | Bilibili |
| X (Twitter) | Weibo |
| Facebook | Kuaishou |
| Threads | Xigua |
| Reddit | Zhihu (columns) |
| LinkedIn | WeChat Official Account (articles) |
| Twitch (clips) | WeChat Channels |
| Pinterest | |
| Bluesky | |
| Snapchat | |
| Kick (clips) | |
| Lemon8 | |

**AgentLens reads**: main text content + media files (images/videos via `downloadUrlList`)
**AgentLens does NOT read**: comment sections, X/Reddit thread conversations

#### API Request
```http
POST https://agentlensapi.io/api/v1/fetch
Authorization: Bearer {AGENT_LENS_API_KEY}
Content-Type: application/json

{ "url": "https://..." }
```

#### Response Fields
```yaml
data.status: HTTP-style status code (200 = success)
data.message: Success message or descriptive error
data.data.platform: Platform identifier (e.g., "youtube", "tiktok")
data.data.name: Author / channel / username
data.data.title: Content title
data.data.description: Full text content
data.data.downloadUrlList[].type: "video" or "pic"
data.data.downloadUrlList[].sourceUrl: Direct media URL
data.data.subtitle: Transcript if available
```
Some error responses use a top-level envelope instead:
```yaml
success: false
error.code: AUTH_FAILED
error.message: API Key invalid or disabled
```
Parse both shapes.

#### Core Retrieval Script
```python
import urllib.request, urllib.error, json

AGENTLENS_ENDPOINTS = [
    "https://agentlensapi.io/api/v1/fetch",
]

def fetch_social_content(url, api_key):
    last_error = None
    for endpoint in AGENTLENS_ENDPOINTS:
        req = urllib.request.Request(
            endpoint,
            data=json.dumps({"url": url}).encode(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.load(resp)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            try:
                result = json.loads(body)
            except json.JSONDecodeError:
                return {"error": f"AgentLens HTTP {e.code}: {body[:300]}"}
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"
            continue

        envelope = result.get("data", result)
        status = envelope.get("status") or result.get("status")
        if str(status) == "200" or result.get("success") is True:
            content = envelope.get("data", envelope)
            return {
                "platform": content.get("platform"),
                "author": content.get("name"),
                "title": content.get("title"),
                "description": content.get("description"),
                "media": content.get("downloadUrlList", []),
                "subtitle": content.get("subtitle")
            }

        error = result.get("error") or {}
        code = error.get("code") or envelope.get("code") or status
        message = error.get("message") or envelope.get("message") or result.get("message") or "Unknown error"
        status_str = str(status)
        code_str = str(code).lower()
        message_str = str(message).lower()

        if status_str == "10032" or "unsupported" in code_str or "unsupported" in message_str or "not supported" in message_str:
            return {"error": message, "code": code, "status": status, "action": "trigger_sop_b"}

        return {"error": message, "code": code, "status": status}

    return {"error": last_error or "AgentLens request failed before receiving a response"}
```

#### Error Handling
- **Status 200**: Success — extract and summarize content.
- **Status 10032 or unsupported-platform message/code**: Trigger SOP B immediately.
- **AUTH_FAILED / HTTP 401**: Ask the user to provide or refresh `AGENT_LENS_API_KEY`; do not retry repeatedly.
- **Other errors** (timeout, parse failure): Inform user the link could not be read at this time.

---

## 7. Video Summarization

**Boundary**: Download or transcribe media only when the current user request requires spoken-content summarization or media analysis. Send audio to OpenAI Whisper only if the user chooses API transcription.

See **SOP C** for the complete flow. Tool details for Steps 3–6:

**Download**:
```bash
curl -L --fail --max-time 120 -o /tmp/asr_{platform}_{timestamp}.mp4 "{sourceUrl}"
```

**YouTube fallback**:
```bash
yt-dlp -f "bv*+ba/best" --merge-output-format mp4 --remux-video mp4 -o "/tmp/asr_youtube_{timestamp}.mp4" "{url}"
```

**Audio extraction**:
```bash
ffmpeg -y -i /tmp/asr_{platform}_{timestamp}.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/asr_audio_{timestamp}.wav
```
> **Required**: ffmpeg must be installed. If missing: `apt install ffmpeg` (Linux), `brew install ffmpeg` (macOS), or download from ffmpeg.org (Windows).

**Local Whisper** (free, CPU):
```bash
pip install faster-whisper
# Model auto-downloads on first use (tiny/base ≈75MB, large-v3 ≈3GB)
```
```python
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, _ = model.transcribe("/tmp/asr_audio_{timestamp}.wav")
transcript = " ".join(segment.text for segment in segments)
```

**OpenAI Whisper API** ($0.006/min, 99+ languages):
```python
import urllib.request, urllib.error, json

def transcribe_whisper(audio_path, api_key, model="whisper-1"):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"model\"\r\n\r\n{model}\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"audio.wav\"\r\n"
        f"Content-Type: audio/wav\r\n\r\n"
    ).encode('utf-8') + audio_data + f"\r\n--{boundary}--\r\n".encode('utf-8')
    req = urllib.request.Request(
        "https://api.openai.com/v1/audio/transcriptions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.load(resp)
        return result.get("text", "")
```

**Note**: OpenAI Whisper API has a 25MB file size limit. For long videos, first normalize/compress the audio, then split into ~5-minute chunks and check each chunk's file size:
```bash
mkdir -p /tmp/asr_audio_chunks
# Normalize to mono 16kHz MP3 at a controlled bitrate
ffmpeg -y -i /tmp/asr_audio_{timestamp}.wav -vn -ac 1 -ar 16000 -c:a libmp3lame -b:a 64k /tmp/asr_audio_{timestamp}.mp3
# Cut into ~5-min chunks (safer than 10-min for the 25MB limit)
ffmpeg -y -i /tmp/asr_audio_{timestamp}.mp3 -f segment -segment_time 300 -c copy /tmp/asr_audio_chunks/chunk_%03d.mp3
# Check chunk sizes; any ≥ 24MB → shorten to 3 min or re-encode at lower bitrate
find /tmp/asr_audio_chunks -name "chunk_*.mp3" -exec ls -lh {} \;
```
If multiple chunks were transcribed → concatenate all text parts in order before summarization.

---

## 8. RSS Feeds — feedparser

**Tool**: feedparser
**API key**: None (free)
**Installation**: `pip install feedparser`
**Code**:
```python
import feedparser

def read_rss(feed_url, limit=10):
    feed = feedparser.parse(feed_url)
    return [
        {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
        }
        for entry in feed.entries[:limit]
    ]

for item in read_rss("FEED_URL"):
    print(f"{item['title']} - {item['link']}")
```

---

## 9. ima OpenAPI — Knowledge Base

ima is Tencent's cloud knowledge base, accessed via OpenAPI (Token + target ID). It works across all channels — inside ima, via Feishu/Lark, Enterprise WeChat, or any third-party agent.

**Boundary**: Use ima only when the current user request asks to save the current item to ima and the target knowledge base is confirmed.

### Service Info

- **Base URL**: `https://ima.qq.com`
- **Base Path**: `/openapi/wiki/v1`
- **Auth Headers**:
  - `ima-openapi-clientid`: Client ID
  - `ima-openapi-apikey`: API Key
  - `Content-Type`: `application/json`
- **Env var mapping**:
  - `IMA_CLIENT_ID` → header `ima-openapi-clientid`
  - `IMA_API_KEY` → header `ima-openapi-apikey`
  - `IMA_KNOWLEDGE_BASE_ID` → request body `knowledge_base_id` / `folder_id`

### Response Format

All APIs return: `{"retcode": 0, "errmsg": "成功", "data": { }}`
- `retcode=0` = success, extract from `data`
- `retcode≠0` = failure, show `errmsg` to user

### Error Codes

| Code | Meaning | Action |
|:-----|:--------|:-------|
| 0 | Success | — |
| 110001 | Invalid parameter | Check request |
| 110021 | Rate limited | Retry after delay |
| 110030 | No permission | Verify Client ID / API Key / KB ID |

### File Size Limits

| Type | Limit |
|:-----|:------|
| Markdown / TXT / Excel | ≤10MB |
| Images | ≤30MB |
| PDF / Word / PPT / Audio | ≤200MB |
| Audio duration | ≤2 hours |

### 9.1 Way A — import_urls (simplest)

Directly import URLs into ima knowledge base; ima parses the content itself. Use when user only wants to archive links.

```bash
curl -X POST "https://ima.qq.com/openapi/wiki/v1/import_urls" \
 -H "ima-openapi-clientid: {IMA_CLIENT_ID}" \
 -H "ima-openapi-apikey: {IMA_API_KEY}" \
 -H "Content-Type: application/json" \
 -d '{
   "knowledge_base_id": "{IMA_KNOWLEDGE_BASE_ID}",
   "folder_id": "{IMA_KNOWLEDGE_BASE_ID}",
   "urls": ["https://example.com/post"]
 }'
```
- `urls`: 1–10 URLs per request
- `folder_id` = `knowledge_base_id` for root directory
- Returns `ret_code` per URL (0 = success) and `media_id`; the top-level envelope uses `retcode`

### 9.2 Way B — Upload Markdown (recommended for AI summaries)

Three-step: create_media → COS upload → add_knowledge.

#### Step 1: create_media

```bash
curl -X POST "https://ima.qq.com/openapi/wiki/v1/create_media" \
 -H "ima-openapi-clientid: {IMA_CLIENT_ID}" \
 -H "ima-openapi-apikey: {IMA_API_KEY}" \
 -H "Content-Type: application/json" \
 -d '{
   "file_name": "{slug}.md",
   "file_size": {byte_size},
   "content_type": "text/markdown",
   "knowledge_base_id": "{IMA_KNOWLEDGE_BASE_ID}",
   "file_ext": "md"
 }'
```
Returns `media_id` and `cos_credential` (含 token, secret_id, secret_key, bucket_name, region, cos_key).

#### Step 2: COS Upload

> ⚠️ **Reference / pending verification**: The curl Authorization header format below is documented for completeness. The actual upload method depends on what `create_media` returns — if it is a pre-signed URL, use that URL directly with the method indicated by the response. For a reliable copy-pasteable upload, use `ima_cos_util` or the official COS SDK (see below) instead of the raw curl below.

Write markdown to temp file, then upload:
```bash
cat > /tmp/asr_{slug}.md << 'EOF'
{markdown_content}
EOF

curl -X PUT "https://{bucket}-{region}.myqcloud.com/{cos_key}" \
 -H "Authorization: COS {secret_id}/{secret_key}/{token}" \
 -H "Content-Type: text/markdown" \
 --data-binary @/tmp/asr_{slug}.md
```

Or use the built-in `ima_cos_util` if available:
```bash
ima_cos_util -f /tmp/asr_{slug}.md
```

#### Step 3: add_knowledge

```bash
curl -X POST "https://ima.qq.com/openapi/wiki/v1/add_knowledge" \
 -H "ima-openapi-clientid: {IMA_CLIENT_ID}" \
 -H "ima-openapi-apikey: {IMA_API_KEY}" \
 -H "Content-Type: application/json" \
 -d '{
   "media_type": 7,
   "media_id": "{media_id}",
   "title": "{title}",
   "knowledge_base_id": "{IMA_KNOWLEDGE_BASE_ID}",
   "folder_id": "{IMA_KNOWLEDGE_BASE_ID}",
   "file_info": {
     "cos_key": "{cos_key}",
     "file_size": {byte_size},
     "file_name": "{slug}.md",
     "last_modify_time": {unix_timestamp}
   }
 }'
```
- `media_type: 7` = Markdown
- `folder_id` = `knowledge_base_id` for root directory

### 9.3 get_addable_knowledge_base_list

Get user's writable knowledge base list (for first-time setup):
```bash
curl -X POST "https://ima.qq.com/openapi/wiki/v1/get_addable_knowledge_base_list" \
 -H "ima-openapi-clientid: {IMA_CLIENT_ID}" \
 -H "ima-openapi-apikey: {IMA_API_KEY}" \
 -H "Content-Type: application/json" \
 -d '{"cursor": "", "limit": 20, "knowledge_base_id": "{IMA_KNOWLEDGE_BASE_ID}"}'
```
Returns `addable_knowledge_base_list` (含 id + name), `next_cursor`, `is_end`.

### 9.4 check_repeated_names

Check if filename already exists in target folder:
```bash
curl -X POST "https://ima.qq.com/openapi/wiki/v1/check_repeated_names" \
 -H "ima-openapi-clientid: {IMA_CLIENT_ID}" \
 -H "ima-openapi-apikey: {IMA_API_KEY}" \
 -H "Content-Type: application/json" \
 -d '{
   "knowledge_base_id": "{IMA_KNOWLEDGE_BASE_ID}",
   "params": [{"name": "{slug}.md", "media_type": 7}]
 }'
```
Returns `is_repeated` (bool). If true, ask user whether to overwrite or rename.

### 9.5 MediaType Reference

| Value | Type |
|:------|:-----|
| 1 | PDF |
| 2 | Web page |
| 3 | Word |
| 4 | PPT |
| 5 | Excel |
| 6 | WeChat Official Account article |
| 7 | Markdown |
| 9 | Image |
| 11 | Note |
| 13 | TXT |

---

## §10. ima Setup — Scene 2 (WorkBuddy) & Scene 3 (External Agent)

These sections document the one-time setup for the two OpenAPI-based ima write paths.

### 10.1 Scene 2 — WorkBuddy Setup (One-time)

**Prerequisite**: ima account + WorkBuddy account must be on the same WeChat ID.

**Step 1 — Install ima skill**:
WorkBuddy left menu → 「专家」→ search "ima" → install 「ima笔记」skill.

**Step 2 — Get API credentials**:
Browser open `https://ima.qq.com/agent-interface` → WeChat scan → copy Client ID and API Key. ⚠️ API Key is shown only once — save immediately.

**Step 3 — Configure credentials**:
In WorkBuddy chat, say: "配置 IMA 凭证，Client ID 是 XXX，API Key 是 XXX".

**Step 4 — Verify connectivity**:
Send "帮我查看我的 IMA 知识库列表" and confirm it returns the KB list.

After setup, save `imaScenario: "workbuddy"` in `~/.agent-social-reader/config.json` only if the user approved local plaintext config storage.

### 10.2 Scene 3 — External Agent Setup (One-time)

Applicable to OpenClaw, Hermes Agent, Claude Code, ChatGPT/Codex, and other third-party agent platforms.

**Step 1 — Get API credentials**:
Browser open `https://ima.qq.com/agent-interface` → WeChat scan → copy Client ID and API Key. ⚠️ API Key shown only once.

**Step 2 — Store credentials**:

**Option A — Environment variables (recommended)**:
```bash
export IMA_CLIENT_ID="your_client_id"
export IMA_API_KEY="your_api_key"
```
Persistence varies by platform:
- **Hermes Agent**: consider persisting to a .env file in the Hermes config directory (path may vary by version — check your Hermes installation for the correct location)
- **Claude Code**: write to `~/.zshrc` or `~/.bashrc`
- **OpenClaw**: write to skill config via `~/.agent-social-reader/config.json` only if the user approved local plaintext config storage
- **ChatGPT/Codex**: add to Custom Instructions or environment config

**Option B — Config files (all platforms, only after user approval for local plaintext storage)**:
```bash
mkdir -p ~/.config/ima
echo "your_client_id" > ~/.config/ima/client_id
echo "your_api_key" > ~/.config/ima/api_key
```
Agent checks env vars first, then falls back to `~/.config/ima/` only if the user approved local plaintext config storage.

**Step 3 — Verify connectivity**:
```bash
IMA_CLIENT_ID="${IMA_CLIENT_ID:-$(cat ~/.config/ima/client_id 2>/dev/null)}"
IMA_API_KEY="${IMA_API_KEY:-$(cat ~/.config/ima/api_key 2>/dev/null)}"
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_addable_knowledge_base_list" \
 -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
 -H "ima-openapi-apikey: $IMA_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{"cursor": "", "limit": 20}'
```
Returns the knowledge base list. Ask user to pick a KB and record its `id`.

**Step 4 — Save KB ID**: If the user approved local plaintext config storage, store the chosen KB ID in `~/.agent-social-reader/config.json` as `imaKnowledgeBaseId`. Set `imaScenario: "external-api"`.

**Optional — Install ima skills package** (includes `ima_api.cjs` and `cos-upload.cjs`):
```bash
curl -o /tmp/ima-skills.zip "https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip"  # version may change; check https://app-dl.ima.qq.com/skills/ for latest
cd /tmp && unzip -o ima-skills.zip
```

### 10.3 PowerShell 5.1 — UTF-8 Encoding Fix

**⚠️ Applies to**: Windows PowerShell 5.1 environments.

**Problem**: All API request bodies must be explicitly converted to UTF-8 bytes, otherwise Chinese characters in content will corrupt.

**Detection**: Check if `$PSVersionTable.PSVersion.Major -lt 7` (PowerShell 5.1 = version < 7).

**Fix**: Encode body explicitly:
```powershell
$body = [System.Text.Encoding]::UTF8.GetBytes((ConvertTo-Json $payload))
$headers = @{
    "ima-openapi-clientid" = $clientId
    "ima-openapi-apikey"   = $apiKey
    "Content-Type"         = "application/json; charset=utf-8"
}
Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body $body
```
In bash/shell environments this is automatic — no special handling needed.
