---
name: anygen-diagram
description: "Use this skill any time the user wants to create diagrams, flowcharts, or visual structures. This includes: architecture diagrams, mind maps, org charts, user journey maps, system design diagrams, ER diagrams, sequence diagrams, process flows, decision trees, network topologies, class diagrams, Gantt charts, SWOT analysis diagrams, wireframes, and sitemaps. Also trigger when: user says 画个流程图, 做个架构图, 思维导图, 组织架构图, 用户旅程图, 系统设计图, 甘特图. If a diagram or visual structure needs to be drawn, use this skill."
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

# AI Diagram Generator — AnyGen

This skill uses the AnyGen CLI to generate diagrams and visual charts server-side at `www.anygen.io`.

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

Follow the `anygen-workflow-generate` skill with operation type `smart_draw`.

If the `anygen-workflow-generate` skill is not available, install it first:

```bash
anygen skill install --platform <openclaw|claude-code> -y
```
