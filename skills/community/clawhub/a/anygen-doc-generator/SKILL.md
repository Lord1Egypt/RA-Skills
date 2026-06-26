---
name: anygen-doc
description: "Use this skill any time the user wants to create, draft, or generate a written document or report. This includes: competitive analysis, market research reports, technical design docs, PRDs, project proposals, meeting summaries, white papers, business plans, literature reviews, due diligence reports, industry analysis, executive summaries, SOPs, memos, and any request where the output is a structured document. Also trigger when: user says 写个文档, 做个竞品调研, 写份报告, 产品需求文档, 技术方案, 项目提案, 行业分析, 会议纪要整理成文档. If a document or report needs to be created, use this skill."
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

# AI Document Generator — AnyGen

This skill uses the AnyGen CLI to generate structured documents and reports server-side at `www.anygen.io`.

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

Follow the `anygen-workflow-generate` skill with operation type `doc`.

If the `anygen-workflow-generate` skill is not available, install it first:

```bash
anygen skill install --platform <openclaw|claude-code> -y
```
