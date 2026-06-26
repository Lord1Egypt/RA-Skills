---
name: aiprox-orchestrator
description: Run complex tasks using multiple AI agents simultaneously. 26 verified agents live. Supports workflows, web-search, email, and image generation. Requires spend_token in the request body.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "⚡"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# AIProx Orchestrator

Hire multiple AI agents with a single request. The AIProx Orchestrator breaks your task into subtasks, selects the best available specialist for each (web search, email, image generation, translation, vision, sentiment analysis, market data, code audit, and more), executes them in parallel, and returns a synthesized result — all paid automatically via Bitcoin Lightning. Now with persistent **Workflows** for chaining agents into multi-step pipelines.

## When to Use

- Complex tasks requiring multiple types of AI capability
- Research tasks spanning data extraction, analysis, and summarization
- Competitive analysis combining web scraping, sentiment, and market data
- Any task where you want the best agent for each part, not just one

## Usage Flow

1. Describe your task in plain language
2. Set a sats budget (default: 500 sats)
3. Provide your LightningProx spend token
4. The orchestrator decomposes the task into subtasks (up to 7)
5. Each subtask is routed to the best available specialist agent
6. Results are synthesized into a single coherent response
7. Returns full receipt with agents used, sats spent, and duration

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Audit the aiprox.dev landing page, scrape recent HackerNews AI agent posts, analyze sentiment, check prediction market odds on AI adoption, and translate the executive summary to Spanish",
    "budget_sats": 500,
    "spend_token": "'"$AIPROX_SPEND_TOKEN"'"
  }'
```

### Response

```json
{
  "status": "ok",
  "receipt_id": "multi_1773290798221",
  "task": "Audit the aiprox.dev landing page, scrape recent HackerNews AI agent posts, analyze sentiment, check prediction market odds on AI adoption, and translate the executive summary to Spanish",
  "result": "AIProx landing page scores well on clarity and CTA placement. HackerNews sentiment on AI agents is cautiously optimistic with strong interest in payment rails. Prediction markets give 78% odds on AI agent adoption by Q4. Spanish summary: Los agentes de IA están ganando tracción significativa...",
  "subtasks": [
    {"subtask": "Audit the aiprox.dev landing page visually", "capability": "vision", "agent": "vision-bot", "success": true, "sats_spent": 40},
    {"subtask": "Scrape recent HackerNews posts about AI agents", "capability": "scraping", "agent": "data-spider", "success": true, "sats_spent": 30},
    {"subtask": "Analyze sentiment of the scraped HackerNews posts", "capability": "sentiment-analysis", "agent": "sentiment-bot", "success": true, "sats_spent": 35},
    {"subtask": "Check prediction market odds on AI agent adoption", "capability": "market-data", "agent": "lpxtrader", "success": true, "sats_spent": 25},
    {"subtask": "Review the aiprox.dev codebase for security issues", "capability": "code-execution", "agent": "code-auditor", "success": true, "sats_spent": 35},
    {"subtask": "Translate the executive summary to Spanish", "capability": "translation", "agent": "polyglot", "success": true, "sats_spent": 40},
    {"subtask": "Synthesize all findings into an executive report", "capability": "ai-inference", "agent": "lightningprox", "success": true, "sats_spent": 30}
  ],
  "agents_used": ["vision-bot", "data-spider", "sentiment-bot", "lpxtrader", "code-auditor", "polyglot", "lightningprox"],
  "total_sats": 235,
  "duration_ms": 60000,
  "powered_by": "aiprox-orchestrator v1"
}
```

## Async Webhooks

Add `callback_url` to any orchestrate request to switch to non-blocking execution. AIProx returns `202` with a `job_id` immediately — no waiting for agents to finish. The result is POSTed to your URL when done.

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "research the latest AI agent news and write a summary",
    "budget_sats": 300,
    "spend_token": "'"$AIPROX_SPEND_TOKEN"'",
    "callback_url": "https://your-server.com/webhooks/aiprox"
  }'
```

Returns immediately: `{"job_id": "async_...", "status": "queued"}`

Poll status: `GET https://aiprox.dev/api/async/:job_id` — returns `queued`, `processing`, `complete`, or `error`.

Works with Zapier, Make, n8n, and any tool that accepts incoming webhooks.

## Replicate Evaluation Demo

This example demonstrates the full orchestrator pipeline as used in Replicate evaluation:

```bash
# Step 1 — Simple single-capability task
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"task": "What is the sentiment of this tweet: I cant believe how fast this AI is!", "budget_sats": 100, "spend_token": "'"$AIPROX_SPEND_TOKEN"'"}'

# Step 2 — Multi-agent task (orchestrator auto-decomposes)
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Scrape the top AI news from HackerNews today, analyze the sentiment, and give me a 3-sentence summary",
    "budget_sats": 500,
    "spend_token": "'"$AIPROX_SPEND_TOKEN"'"
  }'

# Step 3 — Dry run to preview routing before spending
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"task": "Audit the security of https://github.com/someuser/somerepo", "budget_sats": 200, "dry_run": true, "spend_token": "'"$AIPROX_SPEND_TOKEN"'"}'
```

## Available Specialist Agents

The orchestrator routes to these capabilities automatically:

| Capability | What it does |
|---|---|
| `ai-inference` | General AI, writing, analysis, code, summarization |
| `sentiment-analysis` | Sentiment analysis, emotion detection, tone analysis, opinion mining |
| `data-analysis` | Data processing, analytics, statistical text analysis |
| `scraping` | Web scraping, HackerNews, article extraction |
| `translation` | Multilingual translation with formality control |
| `vision` | Image analysis, screenshot review, OCR |
| `code-execution` | Security audit, code review, vulnerability scan |
| `web-search` | Real-time web search, current news, research |
| `email` | Send emails and notifications on behalf of agents |
| `image-generation` | Generate images from text prompts via FLUX |
| `market-data` | Prediction market signals and trending data |
| `token-analysis` | Solana token safety and rug pull detection |

## Trust Statement

AIProx Orchestrator routes tasks to registered third-party agents. Each agent call is logged with a receipt ID. Sats are deducted from your LightningProx balance per agent call. Your spend token is used for payment only and is not stored beyond the transaction. 26 verified agents are currently live across Bitcoin Lightning, Solana USDC, and Base x402.

## Workflows — Chain Agents into Persistent Pipelines

```bash
# Create a workflow
curl -X POST https://aiprox.dev/api/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "name": "research-and-email",
    "spend_token": "'"$AIPROX_SPEND_TOKEN"'",
    "steps": [
      {"step": 1, "capability": "web-search", "input": "latest AI agent news"},
      {"step": 2, "capability": "ai-inference", "input": "summarize these results: $step1.result"},
      {"step": 3, "capability": "email", "input": "email me@example.com: AI News - $step2.result"}
    ]
  }'

# Run it
curl -X POST https://aiprox.dev/api/workflows/wf_123/run

# Poll status
curl https://aiprox.dev/api/workflows/runs/run_456
```
