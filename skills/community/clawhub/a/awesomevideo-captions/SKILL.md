---
name: awesomevideo-captions
description: Burn styled captions onto video (MP4 + SRT/VTT/JSON) via AwesomeVideo MCP or REST. Use when an agent needs subtitles, burned captions, or a free API key for video captioning.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎬"
    homepage: https://awesomevideoeditor.com
    primaryEnv: AWESOMEVIDEO_API_KEY
    requires:
      bins:
        - curl
    envVars:
      - name: AWESOMEVIDEO_API_KEY
        required: false
        description: Optional Bearer token for MCP /mcp and REST. Omit to use keyless /mcp (estimate, create_key, get_catalog). Get one via MCP create_key or POST /v1/keys/anonymous.
---

# AwesomeVideo captions

AwesomeVideo is a video editing API for agents: burn styled captions into video and return the MP4 plus SRT, VTT, and JSON transcript in one call. It exposes MCP (Streamable HTTP) and REST with one key and one balance. Caption price is about **$0.05/min** (5 credits per audio minute; **1 credit = 1 cent**). Translate adds 2 credits/min (7 total).

## 1. Connect keyless (preferred first step)

MCP endpoint (Streamable HTTP):

```text
https://api.awesomevideoeditor.com/mcp
```

Without a key you can still call `initialize`, `tools/list`, `estimate` (with `durationSeconds`), `get_catalog`, and `create_key`. Use `estimate` to price a caption before paying.

Example MCP client config (no key):

```json
{
  "mcpServers": {
    "awesomevideo": {
      "url": "https://api.awesomevideoeditor.com/mcp"
    }
  }
}
```

## 2. Optional API key

Set `AWESOMEVIDEO_API_KEY` when you want paid tools (`caption_video`, etc.) or a reusable Bearer token.

**MCP:** call `create_key` with `{"name":"my-agent"}`. Store the returned `token` once (it is shown only then). New keys may include welcome credits when a fair-share slot is open (often needs a small proof-of-work; see the tool result).

**REST (anonymous):**

```bash
curl -X POST https://api.awesomevideoeditor.com/v1/keys/anonymous \
  -H "Content-Type: application/json" \
  -d '{"name":"my-agent"}'
# -> {"token":"av_live_...","balanceCents":0,...}
export AWESOMEVIDEO_API_KEY='av_live_...'   # do not commit or log this
```

With a key, send `Authorization: Bearer $AWESOMEVIDEO_API_KEY` on REST and as an MCP header:

```json
{
  "mcpServers": {
    "awesomevideo": {
      "url": "https://api.awesomevideoeditor.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Never embed real tokens in this skill, configs checked into git, or chat logs.

## 3. One-call caption recipe

Source must be a **public direct file**, chat attachment URL, or Google Drive / Dropbox share link — **not** YouTube, TikTok, or Instagram (those return 422; upload the file instead).

### MCP

```text
caption_video {
  "sourceUrl": "https://example.com/talk.mp4",
  "preset": "hormozi-pop",
  "language": "en",
  "platform": "tiktok"
}
```

Optional fields: `translateTo` (ISO 639-1), `preset` / `brandPresetId`, `platform`, `wait` / `waitSeconds` (default waits ~45 s). Still running → poll `get_job` with the returned `id`.

### REST

```bash
curl -X POST https://api.awesomevideoeditor.com/v1/captions \
  -H "Authorization: Bearer $AWESOMEVIDEO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sourceUrl": "https://example.com/talk.mp4",
    "preset": "hormozi-pop",
    "wait": true
  }'
```

Success returns burned MP4 URL(s), SRT, VTT, JSON transcript, and `creditsCharged`.

## 4. Prices (always trust live)

Call live pricing (no auth) and prefer those numbers over anything cached:

```bash
curl -sS https://api.awesomevideoeditor.com/v1/pricing
```

Known caption price as of this skill (from live `/v1/pricing`): **transcription 1 + burn 4 = 5 credits per audio minute**; **7 with translate**. Packs and plans exist on that endpoint — do not invent other figures. `estimate` / `quote` / `plan` price a job for free before you run it.

## 5. Links

| What | URL |
| --- | --- |
| Website | https://awesomevideoeditor.com |
| Agent recipes | https://awesomevideoeditor.com/agents |
| Caption API | https://awesomevideoeditor.com/api/captions |
| Facts | https://awesomevideoeditor.com/facts |
| Styles | https://awesomevideoeditor.com/styles |
| n8n workflow | https://awesomevideoeditor.com/integrations/n8n |
| llms.txt | https://api.awesomevideoeditor.com/llms.txt |
| OpenAPI | https://api.awesomevideoeditor.com/openapi.json |
| MCP | https://api.awesomevideoeditor.com/mcp |

## 6. Failure tips

| Symptom | What to do |
| --- | --- |
| **402** `insufficient_balance` | Open `checkoutUrl` from the error (human pays; $5 = 500 credits for this key). Or call MCP `create_checkout`. Retry the same call after payment. |
| **422** on YouTube / TikTok / Instagram URLs | Upload or import the file (`upload` / `import_url`), then pass `fileId` — platform page URLs are not fetched. |
| Job still `queued` / `running` | Poll MCP `get_job` or `GET /v1/jobs/{id}` after `pollAfterSeconds`. Use `webhookUrl` / `notifyEmail` for long jobs. |
| Failed job | Usually refunded. If `resumable: true`, call `resume_job` to continue without re-paying finished steps. |

## Notes for agents

- Prefer MCP `caption_video` for “add subtitles / burn captions on this video”.
- Prefer keyless `/mcp` + `estimate` first; create a key only when you need a paid job or a persistent Bearer token.
- Do not print API keys, tokens, or checkout session secrets.
