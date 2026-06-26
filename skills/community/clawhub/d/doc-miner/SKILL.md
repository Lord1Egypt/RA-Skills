---
name: doc-miner
description: Extract summaries, answers, or structured data from any URL, PDF, or raw text. Auto-detects mode from task.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "📄"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# Doc Miner

Extract insights, answers, and structured data from PDFs, webpages, or raw text. Auto-detects the right mode from your task: summarization, Q&A, or structured extraction of entities, dates, and numbers.

## When to Use

- Summarizing long PDFs or articles
- Answering questions about document contents
- Extracting named entities, dates, or figures
- Analyzing raw text without a URL
- Research and literature review

## Usage Flow

1. Provide a `url` (PDF or webpage) **or** paste `text` directly
2. Optionally specify a `task` — asking a question triggers Q&A mode; "extract" triggers extraction mode; default is summarization
3. AIProx routes to the doc-miner agent
4. Returns mode-specific fields: summary/key_points/word_count, or answer/context/confidence, or entities/dates/numbers

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "task": "extract all dates and key entities",
    "text": "On January 15, 2024, Acme Corp announced a merger with GlobalTech valued at $2.4 billion..."
  }'
```

### Response (extraction mode)

```json
{
  "mode": "extraction",
  "key_points": ["Acme Corp merging with GlobalTech", "Deal valued at $2.4 billion"],
  "entities": ["Acme Corp", "GlobalTech"],
  "dates": ["January 15, 2024"],
  "numbers": ["$2.4 billion"],
  "source_type": "text"
}
```

### Response (summary mode)

```json
{
  "mode": "summary",
  "summary": "Q3 2024 product analytics report covering user metrics and strategic recommendations.",
  "key_points": ["User engagement up 23%", "Mobile conversion 40% below desktop"],
  "word_count": 1240,
  "source_type": "webpage"
}
```

## Trust Statement

Doc Miner fetches and analyzes document contents via URL or processes provided text. Documents are processed transiently and not stored. Analysis is performed by Claude via LightningProx. Your spend token is used for payment only.
