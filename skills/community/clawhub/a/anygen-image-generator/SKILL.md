---
name: anygen-image
description: "Use this skill any time the user wants to generate, create, or design images, illustrations, or visual assets. This includes: posters, banners, social media graphics, product mockups, logo concepts, thumbnails, marketing creatives, profile pictures, book covers, album art, icon designs, and any request for AI-generated imagery. Also trigger when: user says 生成图片, 做个海报, 画个插图, 设计个banner, 做个封面, 社交媒体配图, 产品效果图. If an image or visual asset needs to be created, use this skill."
metadata:
  clawdbot:
    primaryEnv: ANYGEN_API_KEY
    requires:
      bins:
        - anygen
      env:
        - ANYGEN_API_KEY
    install:
      - id: node
        kind: node
        package: "@anygen/cli"
        bins: ["anygen"]
---

# AI Image Generator — AnyGen

This skill uses the AnyGen CLI to generate images and visual assets server-side at `www.anygen.io`.

## Authentication

```bash
# Web login (opens browser, auto-configures key)
anygen auth login --no-wait

# Direct API key
anygen auth login --api-key sk-xxx

# Or set env var
export ANYGEN_API_KEY=sk-xxx
```

When any command fails with an auth error, run `anygen auth login --no-wait` and ask the user to complete browser authorization. Retry after login succeeds.

## How to use

Follow the `anygen-workflow-generate` skill with operation type `ai_designer`.

If the `anygen-workflow-generate` skill is not available, install it first:

```bash
anygen skill install --platform <openclaw|claude-code> -y
```
