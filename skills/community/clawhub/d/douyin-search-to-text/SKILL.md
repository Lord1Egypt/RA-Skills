---
name: douyin-search-to-text
description: "抖音按关键词搜视频再转文字 / Search Douyin by topic, then turn the videos into text. 给一个话题（中文或英文，如 露营装备、AI 编程、camping gear），返回网页已收录的 douyin.com/video 链接和标题；再挑几条读成口播逐字稿、画面文字、要点和点赞评论数。用于找对标视频、选题调研、竞品内容整理。搜索 0 积分；读一条 1 分钟视频 2 积分。不登录抖音、不要 Cookie、不下载视频。需要 LinkDigest API Key（注册送 10 积分）。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/douyin-sousuo-api
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/app/keys 创建，注册送 10 积分，不用绑卡"}],"homepage":"https://linkdigest.dev/zh/douyin-sousuo-api"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/app/keys"
    required_for: "searching and reading; sign-up gives 10 free credits, no card"
---

# Douyin search → text / 抖音搜索转文字

Two steps an agent usually needs together: **find** Douyin videos on a topic, then **read** the ones worth reading.

```bash
export LINKDIGEST_API_KEY=ld_live_...          # https://linkdigest.dev/app/keys — 10 free credits
python3 {baseDir}/scripts/douyin_search.py "露营装备"            # 1. list (free)
python3 {baseDir}/scripts/douyin_search.py "露营装备" --read 2   # 2. list + read the first two
```

The key stays in the environment or the OpenClaw skill `env`; never paste it into chat or code.

## Workflow for the agent

1. **Search.** Run the script with the user's topic. English works: the topic is also searched as the words Douyin creators write (`llm` → 大模型, `camping gear` → 露营装备). Output: a numbered list of titles + `https://www.douyin.com/video/…` links. Costs 0 credits.
2. **Pick.** Show the list. If the user named a number ("read the top 3"), use `--read 3`; otherwise ask which ones, or read single links with `python3 {baseDir}/scripts/linkdigest.py "<link>"`.
3. **Read.** Each read returns the spoken transcript (Qwen3-ASR when there are no platform captions), on-screen text with approximate times, caption, key points, and likes / comments / collects / shares as of today. Long videos queue (HTTP 202); the script polls until done.
4. **Report.** Give the transcript as-is when the user wants 文案; list on-screen text separately; say how many credits were used (stderr, last line). ASR can misspell names, brands and numbers — tell the user to check those.

## Cost

| Step | Credits |
| --- | --- |
| Search (any topic) | 0 |
| Read a video under 1 min | 2 |
| Read a 3-min / 10-min video | 4 / 11 |
| A link anyone has read before (cache) | 0 |
| A link that can't be read | 0 |

Cap a single read with `--max-credits 5`. When credits run out the read answers **402 and charges nothing**; stderr carries the pay links. The smallest top-up is **50 credits for ¥9.9 (支付宝 Alipay) or $1.50 (card)**, one-time, no subscription, never expires; 250 credits are ¥36 / $5. Re-run the same command after paying — reads already done come from cache for free.

## Limits — say these instead of guessing

- It searches what the web has indexed of Douyin's public video pages, not Douyin's in-app search: not the whole platform, not ranked by popularity. Hot topics and specific Chinese wording find the most.
- An empty list means nothing indexed matched; nothing unrelated is padded in. Try a more specific Chinese phrase.
- Per key: 10 searches an hour (`429` → wait). Free accounts also share one daily search pool across the site; paid accounts don't.
- No account pages, no comment sections, no live streams, no private or deleted videos, no video download. The user's own feed: the LinkDigest browser extension, on their own page.
- Exit codes: 0 ok · 2 usage / no key · 3 bad key · 4 out of credits (402, not charged) · 5 unreadable link · 6 rate limited · 7 timed out (re-fetch with `linkdigest.py --job-id <id>`, no double charge).

## JSON instead of Markdown

`--format json` prints the search response (`{"query","platform":"douyin","results":[{"url","title"}],"credits":0}`), and with `--read` each video's full JSON (`transcript[]`, `on_screen[]`, `key_points[]`, `stats`, `credits`, `cached`).

HTTP, if Python isn't available:

```bash
curl -sS -X POST https://linkdigest.dev/api/v1/search \
  -H "Authorization: Bearer $LINKDIGEST_API_KEY" -H "Content-Type: application/json" \
  -d '{"query": "AI 编程", "platform": "douyin", "limit": 5}'
# "digest": true reads every result as one batch and adds a one-page comparison (billed per video)
```

## Privacy

Sends only the topic and the chosen links to linkdigest.dev. Never asks for or reads a Douyin account, cookie or login. Media is held in a temp folder while it is read and deleted before the answer; text results are cached by link. Details: https://linkdigest.dev/privacy

Also as remote MCP (`https://linkdigest.dev/mcp`, tools `search_links` and `digest_url`). Docs: https://linkdigest.dev/zh/douyin-sousuo-api · Support: support@linkdigest.dev
