---
name: bilibili-subtitle-text
description: "B站字幕提取 / Bilibili subtitles to text. 用户要拿到一条 B 站视频的字幕文字（BV 号、bilibili.com/video 链接、b23.tv 短链或整段分享文字），用来复制、翻译、做字幕稿或交给 AI 继续处理时使用。视频有 UP 主字幕就用字幕，没有就做语音识别，每段带开始时间。只读口播，最省钱：每开始 2 分钟 1 积分，不收基础积分。不登录 B 站、不要 Cookie、不下载视频；读不了不扣费。需要 LinkDigest API Key（注册送 10 积分，不用绑卡）。"
version: 1.0.1
homepage: https://linkdigest.dev/zh/bilibili-zimu-tiqu?ref=skill-bilibili-subtitle-text
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/app/keys 创建"}]}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-bilibili-subtitle-text&next=/app/keys"
    required_for: "reading Bilibili subtitles; sign-up gives 10 free credits, no card"
---

# B站字幕提取 · Bilibili subtitles → text

A plain request to a Bilibili video page from a server gets HTTP 412, and most subtitle tools need your Bilibili cookie. This skill sends only the link to LinkDigest and gets the spoken words back as text.

## Quick start

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-bilibili-subtitle-text&next=/app/keys
python3 {baseDir}/scripts/linkdigest.py --depth script "https://www.bilibili.com/video/BV1FtHg6nEE2/"
```

`--depth script` is what makes this the subtitle job: only the spoken words are read, no frames, no summary. (A link someone already read in full comes back as that full read, at 0 credits.) A link, a `b23.tv` short link or the whole share text all work. Add `--format json` for segments as data, `--max-credits 10` to refuse anything longer than that budget, uncharged.

## Use it when / don't

Use it when the user wants the words: to copy, translate, check a quote, or feed another model.

Don't use it for:
- **Notes or a summary.** Use `bilibili-video-to-text` (key points, on-screen text) or `bilibili-course-notes` for lectures.
- **A ready .srt file.** Times are per segment (start only), not per sentence. Say so if the user asks for SRT.

## What the text is

- **Source:** the uploader's own subtitles when the video has them; otherwise speech recognition. The read says which (`transcript_source`; `asr` = recognition, shown as `_source: ASR_` in Markdown).
- **Times:** each segment carries its start time, `` `mm:ss` `` in Markdown, `t` in seconds in JSON (`transcript: [{t, text}]`).
- **Accuracy:** recognition can misspell names, numbers and jargon. Tell the user to check those before quoting.

## Price

| Video length | Credits |
| --- | --- |
| up to 2 min | 1 |
| 10 min | 5 |
| 60 min | 30 |

A link someone already read costs 0. Top-ups are one-time and never expire: 50 credits ¥9.9 (支付宝) / $1.50, 250 credits ¥36 / $5. The cost of each run is printed on the last stderr line.

## When it cannot read

| Answer | Meaning | Charged |
| --- | --- | --- |
| `422` | Deleted, hidden, under review, members-only or region-locked; Bilibili's reason is quoted | no |
| `503` | Bilibili refused this read; try again later | no |
| `402` | Longer than the plan reads, or not enough credits; the reply says which and where to top up | no |

Live rooms, paid 番剧 and comments are not read.

## Privacy

Only the link leaves the machine. No Bilibili account, cookie or login is used. The media is deleted after the read. https://linkdigest.dev/privacy · Remote MCP: `https://linkdigest.dev/mcp` (tool `digest_url`) · support@linkdigest.dev
