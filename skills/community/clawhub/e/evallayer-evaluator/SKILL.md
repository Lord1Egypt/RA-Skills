---
name: evallayer-evaluator
description: "AI-powered deliverable evaluation via EvalLayer API. Extracts factual claims, scores quality, returns structured JSON verdicts with pass/fail, confidence scores, and payout recommendations. Use as a quality gate in agent workflows."
version: 2.0.1
metadata.clawdbot:
  requires.env:
    - EVALLAYER_API_KEY
  requires.bins:
    - curl
    - python3
  primaryEnv: EVALLAYER_API_KEY
---

# EvalLayer Evaluator Skill

AI-powered deliverable evaluation for any OpenClaw agent. Multi-stage verification pipeline extracts factual claims, scores quality, and returns structured JSON verdicts in ~14 seconds.

EvalLayer is a live ERC-8183 evaluator on Virtuals ACP (Agent ID 29588). 250+ evaluations processed. 85% success rate.

## Setup

1. Register for a free API key:
   ```bash
   curl -s -X POST https://api.evallayer.ai/register \
     -H "Content-Type: application/json" \
     -d '{"agent_id": "your-agent-id"}'
   ```
   Save the returned API key — it is shown only once.

2. Set environment variable:
   ```bash
   export EVALLAYER_API_KEY="sk_your_key_here"
   ```

## Evaluate Content

Submit any deliverable for evaluation:

```bash
bash scripts/evaluate.sh "topic" "deliverable content"
```

**Arguments:**
- `topic` (required): What the deliverable should address (e.g., "Solana DeFi ecosystem")
- `deliverable` (required): The content to evaluate

**Example:**
```bash
bash scripts/evaluate.sh \
  "Bitcoin ETF adoption" \
  "BlackRock IBIT accumulated 20 billion in assets within 6 months of launch. Fidelity FBTC reached 10 billion AUM by Q3 2024. Total spot Bitcoin ETF net inflows exceeded 17 billion."
```

**Dependencies:** This script uses `curl` for HTTP requests and `python3` for safe JSON escaping of input text. Both must be available in your PATH.

## Demo (No API Key Required)

Test with 3 free evaluations per day — no registration needed:

```bash
bash scripts/demo.sh "topic" "deliverable content"
```

**Dependencies:** Same as evaluate.sh — requires `curl` and `python3`.

## Quick Evaluate (curl only)

For environments without python3, use curl directly:

```bash
curl -s -X POST https://api.evallayer.ai/evaluate \
  -H "Authorization: Bearer $EVALLAYER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_type": "crypto_research", "topic": "your topic", "deliverable": "content to evaluate"}'
```

Note: this approach does not escape special characters in inputs. Use the script for content containing quotes or backslashes.

## Output Format

```json
{
  "passed": true,
  "quality_score": 0.833,
  "confidence_score": 0.85,
  "rationale": "Evaluated 6 claims: 5 supported, 1 unsupported.",
  "payout_recommendation": "full",
  "claims_total": 6,
  "claims_supported": 5,
  "claims_unsupported": 1,
  "evaluation_id": "eval_abc123_def456"
}
```

**Key fields:**
- `passed`: Boolean — overall pass/fail verdict
- `quality_score`: 0.0-1.0 — overall quality rating (0.4+ = pass, 0.7+ = full payout)
- `claims_total` / `claims_supported`: Claim counts
- `payout_recommendation`: "full", "partial", or "reject"
- `evaluation_id`: Use with GET /evaluate/{id} for detailed claim breakdown

## Check Evaluation Details

Retrieve the full claim-by-claim breakdown for any evaluation:

```bash
curl -s https://api.evallayer.ai/evaluate/EVALUATION_ID
```

Returns each extracted claim with type, support status, confidence score, and notes.

## Check Provider Reputation

Look up any agent's evaluation history:

```bash
curl -s https://api.evallayer.ai/reputation/AGENT_ID
```

## Intelligence API

Access aggregated market intelligence from all evaluations:

```bash
curl -s https://api.evallayer.ai/intelligence \
  -H "Authorization: Bearer $EVALLAYER_API_KEY"
```

Returns trending verified claims, provider leaderboard, and topic trends.

## Rate Limits

- **Free tier:** 5 evaluations/day per API key
- **Demo endpoint:** 3 evaluations/day per IP (no key needed)
- **Pro tier:** 5,000 evaluations/day ($99/mo)

## Use When

- You need to verify research quality before acting on it
- You want to score deliverables in agent-to-agent workflows
- You need to extract and validate factual claims from content
- You are building evaluation gates in ACP or other commerce flows
- You want to check a provider's reputation before hiring them

## NOT For

- Evaluating non-text content (images, audio, video)
- Real-time price data or trading signals
- Content generation — this is verification only

## External Endpoints

- `api.evallayer.ai` — EvalLayer evaluation and intelligence API (HTTPS only)

## Security & Privacy

- Deliverable content is sent to api.evallayer.ai for evaluation over HTTPS
- Content is stored for intelligence aggregation (claims extraction)
- API key authenticates requests and tracks usage — use a dedicated key with minimal scope
- No personally identifiable information is collected
- For sensitive content, review the deliverable before submitting
