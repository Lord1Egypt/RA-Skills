---
name: verify-claim
description: When any factual claim is made — exchange rates, prices, dates, statistics — verify it against live data before using it.
version: 2.0.0
metadata:
  openclaw:
    emoji: "🔍"
    homepage: https://verify.agentutil.net
    always: false
---

# verify-claim

Verify factual claims against live data before using them in responses, calculations, or decisions. Returns structured verdicts with confidence scores and current truth values.

## When to Activate

Use this skill whenever:

- A user states a number as fact ("the exchange rate is 0.92", "Bitcoin is at $60K")
- You are about to use training-data numbers in calculations or recommendations
- A user asks "is it true that..." or "can you verify..."
- You need a current price, rate, date, or statistic for an accurate response
- You are writing a report or analysis that cites specific figures
- A previous response included a number that may have changed since your training cutoff

**Do NOT use for:** opinions, predictions, subjective claims, private/internal data, or questions about future events.

## Workflow

### Step 1: Extract the claim

Identify the specific factual assertion. Be precise — "Bitcoin price is above $60,000" is better than "Bitcoin is expensive."

### Step 2: Check via MCP tool (preferred)

If `@agentutil/verify-mcp` is available as an MCP tool, use it directly:

```
verify_claim({ claim: "The USD to EUR exchange rate is 0.92" })
```

### Step 3: Fall back to HTTP

If no MCP tool is available, call the API:

```bash
curl -X POST https://verify.agentutil.net/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "The USD to EUR exchange rate is 0.92"}'
```

Optional: add `"category"` for faster routing — `financial`, `entity`, `geo`, or `factcheck`.

### Step 4: Interpret the verdict

| Verdict | Confidence | What to do |
|---------|------------|------------|
| `confirmed` | > 0.9 | Safe to use. Cite `current_truth` as the verified value. |
| `confirmed` | 0.7-0.9 | Likely correct but note the uncertainty to the user. |
| `stale` | any | The claim WAS true but data has changed. Use `current_truth` instead. Tell the user: "That was previously correct, but the current value is X." |
| `disputed` | any | Sources disagree. Present both sides — do NOT pick one. Say: "Sources conflict on this — [source A] says X while [source B] says Y." |
| `false` | > 0.8 | Contradicts current data. Correct it: "Actually, the current value is X." |
| `false` | < 0.8 | Likely wrong but not certain. Flag it: "This doesn't match current data (X), but confidence is moderate." |
| `unknown` | any | Could not verify. Say so honestly — do NOT guess. |

### Step 5: Act on the result

- **In calculations:** always substitute `current_truth` for the original claim value
- **In reports:** cite the verified figure with freshness indicator ("as of [freshness]")
- **In conversations:** correct stale data naturally without being preachy
- **If `unknown`:** proceed with the original value but caveat that it's unverified

## Response Format

```json
{
  "verdict": "confirmed",
  "confidence": 0.95,
  "current_truth": "0.921",
  "freshness": "live",
  "source_count": 2,
  "cached": false,
  "request_id": "abc-123",
  "service": "https://verify.agentutil.net"
}
```

## Categories

For faster routing, specify a category:

- `financial` — exchange rates, crypto prices, stock prices
- `entity` — company info, population, founding dates
- `geo` — timezones, geographic data
- `factcheck` — general fact-checking via Google Fact Check API

## Trending Claims

See what others are verifying:

```bash
curl https://verify.agentutil.net/v1/trending
```

## Pricing

- **Free tier:** 25 queries/day, no authentication required
- **Paid tier:** unlimited queries via x402 protocol (USDC on Base), $0.004/query

## Agent Discovery

- MCP server: `@agentutil/verify-mcp` (npm)
- Agent Card: `https://verify.agentutil.net/.well-known/agent.json`
- Service metadata: `https://verify.agentutil.net/.well-known/agent-service.json`

## Privacy

No authentication required for free tier. Query content is not stored beyond transient cache (max 1 hour). No personal data collected. Rate limiting uses IP hashing only.
