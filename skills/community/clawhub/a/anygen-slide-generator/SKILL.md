---
name: anygen-slide
description: "Use this skill any time the user wants to create, design, or produce slide presentations — as standalone files or embedded content. This includes: pitch decks, slide decks, keynote presentations, training materials, project proposals, quarterly reviews, weekly report slides, investor pitches, product launches, team kickoffs, business plans, onboarding decks, strategy presentations, sales pitches, conference talks, and any request involving 'slides' or 'PPT'. Also trigger when: user says 做PPT, 做个汇报, 写个演示文稿, 季度汇报, 竞品分析报告（要PPT）, 产品发布会, 培训材料, 周报. If slides, decks, or presentations need to be produced, use this skill."
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

# AI Slide Generator — AnyGen

This skill uses the AnyGen CLI to generate slide presentations server-side at `www.anygen.io`.

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

Follow the `anygen-workflow-generate` skill with operation type `slide`.

If the `anygen-workflow-generate` skill is not available, install it first:

```bash
anygen skill install --platform <openclaw|claude-code> -y
```
