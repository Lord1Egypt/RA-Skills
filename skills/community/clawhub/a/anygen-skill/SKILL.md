---
name: anygen
version: 2.0.0
description: "AnyGen: AI-powered content creation suite. Create slides/PPT, documents, diagrams, websites, data visualizations, research reports, storybooks, financial analysis, and images. Supports: pitch decks, keynotes, technical docs, PRDs, white papers, architecture diagrams, flowcharts, mind maps, org charts, ER diagrams, sequence diagrams, UML, landing pages, CSV analysis, earnings research, posters, banners, comics, and more. Also trigger when: 做PPT, 写文档, 画流程图, 做网站, 分析数据, 帮我调研, 做绘本, 分析财报, 生成图片, 做海报, 思维导图, 做个架构图, 季度汇报, 竞品调研, 技术方案, 建个落地页, 做个估值, 画个故事."
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

# AnyGen — Content Creation Suite

This skill uses the AnyGen CLI to generate content (slides, docs, diagrams, websites, images, research, and more) server-side at `www.anygen.io`.

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

Follow the `anygen-workflow-generate` skill. Use `anygen task operations` to discover the correct operation type for the user's request.

If the `anygen-workflow-generate` skill is not available, install it first:

```bash
anygen skill install --platform <openclaw|claude-code> -y
```
