---
name: anygen-deep-research
description: "Use this skill any time the user wants in-depth research or comprehensive analysis on any topic. This includes: industry analysis, competitive landscape mapping, market sizing, trend analysis, technology reviews, investment research, sector overviews, due diligence, benchmark studies, patent landscape analysis, regulatory analysis, and academic surveys. Also trigger when: user says 帮我调研一下, 深度分析, 行业研究, 市场规模分析, 竞争格局, 技术趋势, 做个研究报告. If deep research or comprehensive analysis is needed, use this skill."
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

# AI Deep Research — AnyGen

This skill uses the AnyGen CLI to generate in-depth research and analysis reports server-side at `www.anygen.io`.

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

Follow the `anygen-workflow-generate` skill with operation type `deep_research`.

If the `anygen-workflow-generate` skill is not available, install it first:

```bash
anygen skill install --platform <openclaw|claude-code> -y
```
