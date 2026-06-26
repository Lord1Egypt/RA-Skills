---
name: anygen-financial-research
description: "Use this skill any time the user wants financial analysis, earnings research, or investment-related reports. This includes: earnings call summaries, quarterly financial analysis, stock research, equity research reports, financial due diligence, company valuations, DCF models, balance sheet analysis, income statement breakdowns, cash flow analysis, SEC filing summaries, investor memos, portfolio analysis, IPO analysis, M&A research, and credit analysis. Also trigger when: user says 分析财报, 做个估值, 股票研究, 财务尽调, 现金流分析, 收入分析, 季度财务分析. If financial research or analysis is needed, use this skill."
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

# AI Financial Research — AnyGen

This skill uses the AnyGen CLI to generate financial analysis and earnings research reports server-side at `www.anygen.io`.

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

Follow the `anygen-workflow-generate` skill with operation type `finance`.

If the `anygen-workflow-generate` skill is not available, install it first:

```bash
anygen skill install --platform <openclaw|claude-code> -y
```
