---
name: anygen-storybook
description: "Use this skill any time the user wants to create visual stories, illustrated narratives, or storybook content. This includes: storybooks, comics, children's books, illustrated guides, step-by-step visual tutorials, brand stories, product stories, picture books, graphic novels, and visual explainers. Also trigger when: user says 做个绘本, 画个故事, 做个漫画, 做个图文教程, 做个品牌故事. If a visual story or illustrated content needs to be created, use this skill."
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

# AI Storybook Generator — AnyGen

This skill uses the AnyGen CLI to generate visual stories and illustrated narratives server-side at `www.anygen.io`.

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

Follow the `anygen-workflow-generate` skill with operation type `storybook`.

If the `anygen-workflow-generate` skill is not available, install it first:

```bash
anygen skill install --platform <openclaw|claude-code> -y
```
