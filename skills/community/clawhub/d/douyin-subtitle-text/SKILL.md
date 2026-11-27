---
name: douyin-subtitle-text
description: "抖音字幕提取 / 抖音口播文案提取 (Douyin subtitles & speech to text). 用户发来抖音视频链接（douyin.com/video、v.douyin.com 短链或整段分享文字），只要视频里说的话：提字幕、扒口播、拿文案去翻译或改写时使用。抖音不提供字幕文件，这里用语音识别把口播写成文字，每段带开始时间。只读口播、不抽帧，所以最省：每 2 分钟 1 积分，不收基础积分。不登录抖音、不要 Cookie、不下载视频；读不了不扣费。需要 LinkDigest API Key（注册送 10 积分）。"
version: 1.0.2
homepage: https://linkdigest.dev/zh/douyin-zimu-tiqu?ref=skill-douyin-subtitle-text
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-douyin-subtitle-text&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/douyin-zimu-tiqu?ref=skill-douyin-subtitle-text"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-douyin-subtitle-text&next=/app/keys"
    required_for: "reading the speech of a Douyin video; sign-up gives 10 free credits, no card"
---
# 抖音字幕提取 · 口播文案 (Douyin speech → text)

Douyin does not publish a subtitle file. The "字幕" on a video is either pixels on the frames or nothing at all, so "extract the subtitles" really means: write down what was said. This skill does that from the link alone.

## Quick start

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-douyin-subtitle-text&next=/app/keys
python3 {baseDir}/scripts/linkdigest.py --depth script "https://v.douyin.com/VeXgdE_QwTE"
```

`--depth script` is the whole point: only the speech is read, no frames and no on-screen text, which makes it the cheapest read there is. The answer is Markdown with the caption and a transcript whose lines start with `` `mm:ss` `` (an `≈` in front marks an estimated time). Add `--format json` for `transcript: [{t, text}]` as data, and `--max-credits 5` to refuse anything dearer.

Accepted: a `douyin.com/video/...` link, a `v.douyin.com` short link (copy it exactly, the code is case-sensitive), or the whole text the app's 分享 → 复制链接 gives. A link that was already read in full comes back as that full read, at 0 credits.

## Price

| Video length | Credits |
| --- | --- |
| up to 2 minutes | 1 |
| 5 minutes | 3 |
| 10 minutes | 5 |

1 credit per started 2 minutes, no base credit. Sign-up gives 10 credits once, no card. Top-ups are one-time and never expire: 50 credits ¥9.9 (支付宝) / $1.50, 250 credits ¥36 / $5. Each run prints its cost on the last line of stderr.

## Right tool, wrong tool

Use it when the user wants the words themselves: to copy the 文案, translate it, check a quote, or hand it to another model.

Use something else for:

- **The text burned into the picture** (hard subtitles, slides, price tags). That needs the frames: `douyin-video-to-text` reads speech and on-screen text together.
- **"What does this video say?"** `douyin-video-summary` answers with points and the lines behind them.
- **An .srt file.** Times are per segment (start only), not per sentence. Say so if asked for SRT.
- **Dozens of links.** `douyin-batch-to-text`.

## Without a key

The script still runs with no `LINKDIGEST_API_KEY`: it falls back to the free summary (title, author, key points; up to 2 a day per address), which has **no transcript**. For the words themselves a key is needed. Say that plainly instead of presenting the summary as the subtitles.

## About the text

- It is speech recognition (`transcript_source: asr`). Names, numbers and technical terms can come out wrong; tell the user to check them before quoting.
- A video with music and no speech gives an empty or near-empty transcript. Pass that on as it is; do not invent lines.
- Punctuation and paragraphing are the recogniser's. Tidy them only if the user asks, and say that you did.

## When it cannot read

| Answer | Meaning | Charged |
| --- | --- | --- |
| `422` | Deleted, private, a live room, or shown only to signed-in users; the reason is quoted | no |
| `503` | Douyin declined this read; try again later | no |
| `402` | Not enough credits, or longer than the account reads; the reply says which | no |
| `401` | The key is wrong | no |

## Privacy

Only the link leaves the machine. No Douyin account, cookie or login is used, and nothing is downloaded locally; the media is deleted after the read. https://linkdigest.dev/privacy · Remote MCP: `https://linkdigest.dev/mcp` (tool `digest_url`, `depth: "script"`) · support@linkdigest.dev
