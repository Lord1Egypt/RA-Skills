---
name: aggclaw
version: "1.2.1"
display_name: "AppGrowing 全球广告素材智能分析助手"
display_name_en: "AppGrowing Global Ad Creative Analysis Assistant"
description: "AppGrowing Global intelligent ad creative analysis assistant. Finds the most relevant global ad creatives based on your instruction and delivers automated analysis. Includes Inspire ideation mode. Triggers: keywords analyze creatives, creative analysis, global campaigns, explore creatives, find creatives; commands /aggclaw, /agg_inspire"
description_zh: "AppGrowing Global 智能广告素材分析助手，基于你的指令检索最相关的全球广告素材并自动完成分析，支持灵感激发（Inspire）模式。触发词：分析素材、素材分析、全球投放、找素材、探索素材；命令：/aggclaw、/aggclaw-game、/aggclaw-app、/agg_inspire"
description_en: "AppGrowing Global intelligent ad creative analysis assistant. Finds the most relevant global ad creatives based on your instruction and delivers automated analysis. Includes Inspire ideation mode. Triggers: keywords analyze creatives, creative analysis, global campaigns, explore creatives, find creatives; commands /aggclaw, /agg_inspire"
homepage: https://appgrowing.net/
metadata:
  {
    "openclaw": {
      "slug": "aggclaw",
      "version": "1.2.1",
      "author": "youcloud",
      "emoji": "🌍",
      "requires": {
        "env": ["YOUCLOUD_API_KEY"]
      }
    }
  }
---

# aggclaw

AppGrowing Global intelligent ad creative analysis assistant; analyzes global ad creatives, includes Inspire mode. Available to AI plus / Pro subscribers.

## Prerequisite: API Key

Read from env var `YOUCLOUD_API_KEY`. **Never send requests without a valid key.** When missing, prompt:

```
Please configure your API Key first:
1. Get it from AppGrowing Global → Profile → Enterprise Info
2. Set env var: Linux/macOS `export YOUCLOUD_API_KEY="..."`; Windows `$env:YOUCLOUD_API_KEY="..."`
3. Resend your request
```

## Triggers & Modes

| Trigger | chat_mode |
|---|---|
| `/aggclaw` (auto-detect, see below) | — |
| `/aggclaw-game` | 7 Game |
| `/aggclaw-app`, `/aggclaw-shortdrama` | 8 Non-game |
| `/agg_inspire` | 9 Inspire |
| Keywords (analyze creatives, creative analysis etc.) | Auto-detect |

**`/aggclaw` auto-detect:** discussion-style question (advice/strategy/ideas/comparison/"how to", not asking for specific creative data) → 9; game content (game titles, RPG/SLG/MMO) → 7; other → 8.

## Language Detection

Detect the user's input language and reply in that language throughout (framing text, errors, summaries included); keep `input` in the user's original wording — do not translate. Preference persists for the whole session.

| Input contains | language_code |
|---|---|
| Chinese characters | `zh` |
| Hiragana / Katakana | `ja` |
| Other | `en` |
| Undetermined | omit |

`language_code` may only be `zh`/`ja`/`en`; omit for any other language.

## Execution Flow

1. **Check API Key** (above)
2. **Detect language + determine chat_mode** (above)
3. **Call the API directly** — do not ask the user for product positioning, target market, or other supplementary info; let the API search on its own:
   - New analysis → send `input` + `chat_mode` + `language_code`, no `session_id`
   - Follow-up → reuse `session_id`, omit `chat_mode`/`language_code` (preserve the session's mode & language)
   - Output `output`; translate if its language differs from the user's; save `session_id` for follow-ups

⚠️ **Mandatory timeout rule:** set timeout to **600s** (responses often take 60s+). **Never** interrupt before timeout. **Never** send "still processing" / "will let you know" messages. Wait for the complete result, then reply in one shot; only "result returned" or "timeout/error" situations may send a message.

## Analysis Endpoint

- URL: `https://ai-chat-global.youcloud.com/aichat/claw`
- Method: POST JSON
- Headers: `Authorization: Bearer {KEY}`, `Content-Type: application/json`
- Params: `input` (required), `session_id` (follow-ups), `chat_mode` (7/8/9, new sessions only), `language_code` (zh/ja/en, new sessions only)
- Timeout: ≥600s

## Materials Download

After an analysis completes (`session_id` available), the user may ask to download that conversation's creatives.

**Intent routing:**
- "Download materials" without a scope → **do not start downloading**; ask the user to choose a scope first. Prefer the host's ask/question tool to pop an interactive card; if the host lacks one (e.g., IM clients), fall back to a plain text message listing the options. All display text must be in the detected language:
  - Title: information retrieved from the last conversation — which would you like to download?
  - Option 1: creatives mentioned in the analysis result → download `is_mentioned=true`
  - Option 2: all creatives → download the entire list (no filtering)
- "Download mentioned creatives" or close semantics → download `is_mentioned=true`

**Materials endpoint:**
- URL: `https://ai-chat-global.youcloud.com/aichat/sessions/{session_id}/materials`
- Method: GET; Header `Authorization: Bearer {KEY}`; Timeout ≥120s
- Encode `=` in `session_id` as `%3D` (keep `~`). Example: `99QLLyMfj8uUrvalSiHr~g%3D%3D`
- Response: JSON array `[{id, detail_url, download_url, is_mentioned}]`; **always returns the full list** — filter by `is_mentioned` client-side

**Download rules:**
- On HTTP 403 (link expired) → **silently** re-fetch materials and retry the failed item, no message to the user
- Concurrency ≤ 3; queue when exceeded
- **No messages during download**; on completion send **one** message in the detected language: local path + download count (success x, failure y; append failed ids if y>0)
- Save to a new folder named after the first `## ` heading of the analysis report (strip `## `, replace illegal chars `/ \ : * ? " < > |` with `_`); filename `{id}.{ext}` (ext from download_url, else response Content-Type)

## Auth (two models — do not mix)

| URL | Auth |
|---|---|
| `/aichat/claw`, `/sessions/{id}/materials` | `Authorization: Bearer {KEY}` header |
| `download_url` (CDN direct link) | **No header** — relies on the `auth_key` embedded in the URL |

## PowerShell Template

```powershell
# Analysis
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$body = @{input="Your analysis request"; chat_mode=8; language_code="en"} | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "https://ai-chat-global.youcloud.com/aichat/claw" -Method Post -ContentType "application/json; charset=utf-8" -Headers @{Authorization="Bearer $env:YOUCLOUD_API_KEY"} -Body $body -TimeoutSec 600 | Select-Object -ExpandProperty output

# Materials list + download (no auth header on download_url)
$enc = [uri]::EscapeDataString($sessionId)
$resp = Invoke-RestMethod -Uri "https://ai-chat-global.youcloud.com/aichat/sessions/$enc/materials" -Headers @{Authorization="Bearer $env:YOUCLOUD_API_KEY"} -TimeoutSec 120
foreach ($m in $resp) { Invoke-WebRequest -Uri $m.download_url -OutFile "$folder\$($m.id).mp4" -TimeoutSec 180 }
```

## Error Handling

- 400/401 auth failed: `API Key authentication failed. Check if your key is active or expired. Get it from AppGrowing Global Profile → Enterprise Info, or contact support.`
- Other: `Request returned an error (code={code}). Check your API Key permissions, account quota, or contact support.`

## Material Link Template

When an analysis result contains a material ID, splice it into the detail-page link below so the user can click through to view the creative video / ad delivery data:

- **Template**: `https://appgrowing-global.youcloud.com/material/{{ID}}`
- **Usage**: Replace `{{ID}}` with the actual material ID. For example, ID `abc123` → `https://appgrowing-global.youcloud.com/material/abc123`
- **Output**: Render as a Markdown link, e.g. `[material abc123](https://appgrowing-global.youcloud.com/material/abc123)`, so the user can click to jump to the detail page.

## Examples

For full input/output examples, see [references/example.md](references/example.md)
