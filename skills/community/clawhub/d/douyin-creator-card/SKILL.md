---
name: douyin-creator-card
description: "抖音博主主页信息 / Douyin creator profile card. 用户发来抖音博主的主页分享链接（抖音 App 里打开博主主页 → 分享 → 复制链接，形如 douyin.com/user/MS4w… 或 iesdouyin.com/share/user/…），想知道这个账号的粉丝数、获赞数、作品数、简介、抖音号、IP 属地时使用。不登录抖音、不要 Cookie、不下载任何内容。1 积分一次，读不了不扣费。只给主页信息，不含作品列表：作品要一条一条发视频链接。需要 LinkDigest API Key（注册送 10 积分，不用绑卡）。"
version: 1.0.0
homepage: https://linkdigest.dev/platforms?ref=skill-douyin-creator-card
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/app/keys 创建"}]}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-douyin-creator-card&next=/app/keys"
    required_for: "reading a Douyin creator's profile; sign-up gives 10 free credits, no card"
---

# 抖音博主主页信息 · Douyin creator profile card

A Douyin profile page (`douyin.com/user/…`) answers a plain request with an empty shell, so an agent handed one cannot say who the creator is or how large the account is. This skill reads the public profile through LinkDigest and returns it as text.

## What you get

The shape of a real read on 2026-11-25 (the creator's name is left out here):

```text
title    <博主名> (@<抖音号>)
bio      <主页简介，原文逐行>
counts   1,199,087 followers · 9 following · 2,430,327 likes received · 105 posts
抖音号    <抖音号>
IP属地    山东
```

plus a few key points written from the bio. The counts are the ones the profile shows on the day of the read.

## Which links work

| The user pasted | Result |
| --- | --- |
| `douyin.com/user/MS4w…` (from the app: profile → 分享 → 复制链接) | Profile card, 1 credit |
| `iesdouyin.com/share/user/MS4w…` | Profile card, 1 credit |
| `douyin.com/user/<a name or a short number>` | Not a page Douyin serves. Answered `422`, not charged; ask the user for the share link from the app |
| A video link (`v.douyin.com/…`, `douyin.com/video/…`) | That is a video: use `douyin-video-to-text` |

## Run it

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-douyin-creator-card&next=/app/keys
python3 {baseDir}/scripts/linkdigest.py --format json "https://www.douyin.com/user/MS4wLjABAAAA..."
```

Takes about 8–20 seconds the first time; a profile someone already read today comes back at once.

## How to answer the user

1. Give the name, 抖音号 and the four counts first; say they are as of today.
2. Quote the bio as written. Do not guess the creator's niche beyond what the bio and key points say.
3. If they want what the creator posts, say that this skill reads the profile only, and ask for one or more video share links (`douyin-video-to-text` reads those, `douyin-search-to-text` finds videos by topic).

## Limits, stated plainly

- **No post list.** The creator's videos are not included; Douyin does not show them to a signed-out reader.
- **No follower history, no audience data.** One snapshot of what the public profile shows.
- **Private or banned accounts** answer `422` with Douyin's reason. Not charged.

## Cost

1 credit per profile read; a refused read is free. Top-ups are one-time and never expire: 50 credits ¥9.9 (支付宝) / $1.50, 250 credits ¥36 / $5.

## Privacy

Only the link goes to linkdigest.dev. No Douyin account, cookie or login is used. https://linkdigest.dev/privacy · Remote MCP: `https://linkdigest.dev/mcp` (tool `digest_url`) · support@linkdigest.dev
