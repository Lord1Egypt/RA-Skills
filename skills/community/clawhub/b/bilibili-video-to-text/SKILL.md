---
name: bilibili-video-to-text
description: "B站视频转文字 / Bilibili video to text. 用户发来 bilibili.com/video/BV… 或 b23.tv 短链，要提取视频文案、做笔记、总结 UP 主讲了什么、整理课程或评测内容时使用。返回口播逐字稿（分段带时间）、画面上的字、标题简介、要点和互动数据。不登录 B 站、不要 Cookie、不下载视频。1 分钟视频 2 积分（约 ¥0.29），读不了不扣费；需要 LinkDigest API Key（注册送 10 积分，不用绑卡）。"
version: 1.0.0
homepage: https://linkdigest.dev/platforms?ref=skill-bilibili-video-to-text
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-bilibili-video-to-text&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/platforms?ref=skill-bilibili-video-to-text"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-bilibili-video-to-text&next=/app/keys"
    required_for: "reading Bilibili videos; sign-up gives 10 free credits, no card"
---

# B站视频转文字 (Bilibili video → text)

Bilibili answers ordinary server requests with HTTP 412, so fetching a `bilibili.com/video/BV…` link from an agent returns nothing. This skill reads the video through LinkDigest, which uses the player Bilibili itself publishes for other sites, and hands back text.

## One command

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-bilibili-video-to-text&next=/app/keys
python3 {baseDir}/scripts/linkdigest.py "https://www.bilibili.com/video/BV1FtHg6nEE2/"
```

Works with a full link, a `b23.tv` short link, or the whole share text copied from the app (the script finds the link in it). Add `--format json` for structured output, `--max-credits 6` to skip anything longer than that budget without being charged.

## What comes back

| Field | Notes |
| --- | --- |
| Transcript | Spoken words; Bilibili's own subtitles when the video has them, otherwise speech recognition (Qwen3-ASR). Timed by segment, not by sentence. |
| On-screen text | Captions, titles and on-screen words read from the frames, with approximate times. |
| Title, uploader, description | As Bilibili shows them. |
| Key points | A few lines on what the video says, each tied to the transcript. |
| Stats | Views, likes, coins, favourites where the player shows them, as of today. |

## How the agent should use it

1. Run the script on the link the user gave. A long video may answer `202` first; the script waits and polls until it is done.
2. Hand the transcript over as-is when the user wants 文案 or notes; keep on-screen text separate.
3. Say what it cost (last line on stderr) and remind the user that recognition can misspell names and numbers.

## When it cannot read

- Deleted, hidden, under-review, members-only or region-locked videos: answered `422` with Bilibili's own reason. Not charged.
- Bilibili occasionally refuses the read itself: answered `503` with a retry hint. Not charged; try again later.
- Videos longer than the plan reads (30 minutes on most plans) answer `402` and offer a transcript-first read (`--depth transcript`) instead. Nothing is charged until you choose.
- Live rooms, 番剧 behind a paywall, and comment sections are not read.

## Cost

2 credits for the first minute, then 1 per started minute (a 3-minute video is 4). A link someone has already read is free. The smallest top-up is 50 credits for ¥9.9 (支付宝) or $1.50; 250 credits are ¥36 / $5. One-time, no subscription, never expire.

## Privacy

Only the link goes to linkdigest.dev. No Bilibili account, cookie or login is ever asked for or used. The video is held in a temp folder while it is read and deleted before the answer. https://linkdigest.dev/privacy

Also available as remote MCP: `https://linkdigest.dev/mcp` (tool `digest_url`). Support: support@linkdigest.dev
