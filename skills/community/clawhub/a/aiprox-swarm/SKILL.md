---
name: aiprox-swarm
description: 40-persona prediction engine for binary market questions. Returns YES/NO/SKIP with confidence score and reasoning from a simulated trader swarm.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "🐝"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# SWARM

Submit a binary YES/NO market question to a 40-persona AI trader swarm. Each persona reasons independently — bulls argue for YES, bears argue for NO, neutral analysts vote freely. Confidence-weighted votes are aggregated into a final verdict with reasoning and a groupthink warning when consensus is suspiciously one-sided.

**Personas:** 18 bulls · 18 bears · 4 neutral analysts  
**Domains:** crypto, macro, political, sports, general  
**Access:** via AIProx orchestrator — capability: `prediction`

## When to Use

- Polymarket-style binary questions: "Will X happen before Y?"
- Bitcoin and crypto price targets
- Macro events: Fed decisions, CPI outcomes, rate cuts
- Election and political outcomes
- Any question where you want a structured bull/bear debate rather than a single model's opinion

## Usage Flow

1. Provide `task` — the binary question (minimum 10 words)
2. Optionally provide `context` — recent news, price levels, or market data appended as `recent news: ...`
3. SWARM fans the question out to 40 personas in parallel (~30–60s)
4. Returns `prediction` (YES/NO/SKIP), `confidence` (1–85), `reasoning`, `voter_summary`, `domain`, and `groupthink_warning`

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | SWARM queries via AIProx orchestrator |

## Make Request — Basic

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "task": "Will Bitcoin exceed $150,000 before the end of 2025?",
    "capability": "prediction"
  }'
```

### Response — Basic

```json
{
  "prediction": "YES",
  "confidence": 38,
  "reasoning": "ETF Flow Tracker: Spot ETF inflows averaging $800M/week create structural demand that historically precedes new highs. | Global Liquidity Bull: M2 expansion in China and Europe is feeding into risk assets with a 6-month lag. | Leverage Flush Analyst: Open interest is elevated and funding rates are positive — a flush before the move up is likely but doesn't change the directional call.",
  "voter_summary": "Bull avg: 61 (18 active, 0 SKIP) | Bear avg: 23 (18 active, 0 SKIP) | Neutral: 3 YES / 1 NO / 0 SKIP | Margin: 38pts",
  "domain": "crypto",
  "persona_count": 40,
  "groupthink_warning": false
}
```

## Make Request — With Context

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $AIPROX_SPEND_TOKEN" \
  -d '{
    "task": "Will the Fed cut rates at its June meeting?\n\nRecent news: CPI printed 2.4% in March, below expectations. Jobs report added 175k jobs, unemployment ticked up to 4.1%. Fed chair Powell said the committee needs more confidence inflation is moving sustainably to 2% before cutting.",
    "capability": "prediction"
  }'
```

### Response — With Context

```json
{
  "prediction": "NO",
  "confidence": 29,
  "reasoning": "Higher-For-Longer Bear: Powell's explicit signal of needing more confidence, combined with still-solid employment, gives the committee cover to hold. | Macro Bear: The jobs market has not deteriorated enough to force the Fed's hand — June remains a stretch. | Economist: Base rates favor holding: the Fed has cut at only 3 of the last 12 June meetings when unemployment was below 4.2%.",
  "voter_summary": "Bull avg: 31 (17 active, 1 SKIP) | Bear avg: 60 (18 active, 0 SKIP) | Neutral: 1 YES / 3 NO / 0 SKIP | Margin: 29pts",
  "domain": "macro",
  "persona_count": 40,
  "groupthink_warning": false
}
```

## Example Prompts

```
Will Bitcoin exceed $150,000 before the end of 2025?
```

```
Will Ethereum outperform Bitcoin over the next 90 days?
Context: ETH/BTC ratio is at 0.038, a 4-year low. Pectra upgrade ships next month.
```

```
Will the S&P 500 be higher than today in 6 months?
Context: Current level 5200. Fed on hold. Q1 earnings beat expectations by 7%.
```

```
Will there be a US recession before the end of 2026?
```

```
Will Solana flip Ethereum by market cap before 2027?
```

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `prediction` | string | `YES`, `NO`, or `SKIP` |
| `confidence` | number | 1–85. Margin between bull and bear weighted averages. |
| `reasoning` | string | Top 3 reasons from the winning camp, highest-confidence personas first. |
| `voter_summary` | string | Bull avg, bear avg, neutral split, and margin in one line. |
| `domain` | string | Detected domain: `crypto`, `macro`, `political`, `sports`, or `general`. |
| `persona_count` | number | Always 40. |
| `groupthink_warning` | boolean | `true` when >80% of non-SKIP votes point the same direction. |

## Notes

- **SKIP is a valid result.** It means the bull and bear camps are within 15 confidence points — the swarm is genuinely split.
- **Groupthink warning** fires when consensus is very high. This can mean the question is already settled, or that the swarm lacks the context to form a contrarian view. Add news context and re-run.
- **Minimum 10 words.** Very short questions without context return a 400 error — the swarm needs enough signal to reason against.
- **~30–60 seconds per call.** 40 parallel LLM calls run concurrently via DeepSeek.
- **Domain weighting.** Crypto questions weight crypto-domain personas at 1.5×. Macro questions weight macro experts. General questions use equal weights.

## Trust Statement

SWARM processes your question transiently. Questions and responses are not stored beyond the active request. No authentication or API key required for the default public endpoint.
