---
name: aiprox-workflows
description: Create and run multi-agent AI workflows on AIProx. Chain agents into scheduled pipelines. Pay per execution in sats.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "⚡"
    homepage: https://aiprox.dev/workflows
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# AIProx Workflows

AIProx Workflows is a multi-agent pipeline engine. Chain AI agents into named workflows, schedule them to run on a cron, and get results delivered by email or webhook. Pay per execution in sats — no subscriptions, no monthly fees.

## When to Use

- Building automated pipelines that chain multiple AI agents
- Scheduling recurring tasks (daily news digest, competitive intel, market signals)
- Running one-off multi-step pipelines on demand
- Any workflow where one agent's output feeds into the next

## MCP Tools

### `create_workflow`

Create a named pipeline with ordered agent steps.

```
Create a workflow "daily-crypto-brief" that searches Bitcoin news, analyzes sentiment, and emails a summary @daily
```

Step chaining: use `$step1.result`, `$step2.result`, etc. to pass outputs forward.

**Available capabilities:**

| Capability | What it does |
|---|---|
| `web-search` | Real-time web search via search-bot |
| `sentiment-analysis` | Sentiment and tone analysis via sentiment-bot |
| `scraping` | Web scraping and article extraction via data-spider |
| `data-analysis` | Data processing and text analysis via doc-miner |
| `translation` | Multilingual translation via polyglot |
| `vision` | Image/screenshot analysis via vision-bot |
| `code-execution` | Code audit and security review via code-auditor |
| `email` | Send email notifications via email-bot |
| `market-data` | Prediction market signals via market-oracle |
| `token-analysis` | Solana token safety and rug detection via isitarug |

### `run_workflow`

Trigger any workflow by its ID.

```
Run workflow wf_abc123
```

### `list_workflows`

Show all workflows for the current spend token.

```
List my workflows
```

### `get_run_history`

Show past execution results, sats spent, and step-by-step output.

```
Show run history for wf_abc123
```

### `delete_workflow`

Delete a workflow (cancels scheduled runs).

### `run_template`

Run a pre-built template by name in one shot.

```
Run the polymarket-signals template and email me at user@example.com
```

## Pre-Built Templates

| Template name | Pipeline | Cost |
|---|---|---|
| `news-digest` | search-bot → sentiment-bot → email-bot | ~150 sats/run |
| `token-scanner` | data-spider → isitarug → email-bot | ~120 sats/run |
| `competitive-intel` | search-bot → doc-miner → sentiment-bot → email-bot | ~200 sats/run |
| `multilingual-content` | data-spider → doc-miner → polyglot | ~180 sats/run |
| `site-audit` | vision-bot → code-auditor → doc-miner | ~220 sats/run |
| `polymarket-signals` | market-oracle → sentiment-bot → email-bot | ~160 sats/run |
| `api-security-audit` | data-spider → code-auditor → pdf-bot → email-bot | ~300 sats/run |

## Authentication

Set `AIPROX_SPEND_TOKEN` in your MCP server config. Get a spend token at [lightningprox.com](https://lightningprox.com).

```json
{
  "mcpServers": {
    "aiprox-workflows": {
      "command": "npx",
      "args": ["aiprox-workflows-mcp"],
      "env": {
        "AIPROX_SPEND_TOKEN": "lnpx_your_token_here"
      }
    }
  }
}
```

## Scheduling

| Shorthand | When |
|---|---|
| `@hourly` | Every hour |
| `@daily` | Every day at midnight |
| `@weekly` | Every Sunday |
| `0 9 * * 1-5` | 9am Monday–Friday |

## Pricing

50–220 sats per workflow execution depending on agents used. No monthly plan. Deducted from your Lightning spend token balance.

## Behavior Guidelines

**When a user asks to automate something:**
1. Identify which capabilities are needed (search → analyze → notify is the common pattern)
2. Suggest a template if one matches, otherwise offer to create a custom workflow
3. Confirm the schedule and email/webhook if they want recurring runs
4. After creating, offer to run it immediately

**Cost transparency:**
- Mention estimated sats cost before creating/running
- Report `sats_spent` after each run

**Check templates first:**
If the task matches a template, use `run_template` — it's faster and pre-configured.

## Async Execution

For one-off orchestrate requests (not scheduled workflows), add `callback_url` to get a `job_id` back immediately and receive the result via webhook when done. Poll status at `GET https://aiprox.dev/api/async/:job_id`. Works with Zapier, Make, and n8n.

## Links

- Dashboard: [aiprox.dev/workflows](https://aiprox.dev/workflows)
- Templates: [aiprox.dev/templates](https://aiprox.dev/templates)
- Registry: [aiprox.dev/registry.html](https://aiprox.dev/registry.html)
- npm SDK: `npm install aiprox-workflows`
- MCP server: `npx aiprox-workflows-mcp`
