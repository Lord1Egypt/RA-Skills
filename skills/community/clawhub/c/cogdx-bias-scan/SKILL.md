---
name: cogdx-bias-scan
description: Detect systematic inference-level biases in an AI agent's reasoning via Cerebratech CogDx API ($0.10 per call, credits accepted). Use when an agent keeps making the same type of error across different contexts, when users report consistent blind spots or assumptions, when outputs show anchoring, recency, confirmation, or availability bias patterns, or before deploying to a new domain. Uses statistical pattern matching against 188+ known cognitive bias signatures — no LLM in the backend. Triggers on phrases like "scan for bias", "detect my biases", "why do I keep making this mistake", "anchoring bias", "confirmation bias", "I always assume X", "systematic errors", or any request to identify recurring reasoning patterns. After running, use cogdx-feedback skill (FREE) to verify retraining and earn credits.
repository: https://github.com/drkavner/cogdx
license: MIT
author: Dr. Kavner / Cerebratech
---

# CogDx Bias Scan

External detection of systematic inference-level biases. Identifies which of 188+ cognitive bias patterns are active in your reasoning traces. Pure statistical matching — no LLM backend.

## Cost

- **$0.10 per call** (x402 payment on Base/USDC, or use credit balance)
- Credits from `/feedback` submissions apply
- Payment address: `Cerebratech.eth`

## When to Use

- Same error pattern recurring across different prompts or contexts
- Users report "you always assume X" or "you never consider Y"
- Pre-deployment bias audit for high-stakes domains
- After any significant context shift (new users, new domain, new instruction set)

## Bias Categories Detected

- **Anchoring** — Overweighting first information received
- **Recency** — Overweighting recent examples vs. historical base rates
- **Confirmation** — Seeking/interpreting evidence to confirm priors
- **Availability** — Overweighting easily recalled examples
- **Framing** — Response changes based on presentation, not content
- **Attribution** — Systematic over/under-attribution of causality
- **+ 182 others** (see `references/bias-catalog.md`)

## API Call

**1. Check credit balance:**
```bash
GET https://api.cerebratech.ai/credits?wallet=your-agent-id
```

**2. Run the scan:**
```bash
POST https://api.cerebratech.ai/bias_scan
Content-Type: application/json
X-PAYMENT: <x402-signature>  # or omit if using credits
X-WALLET: your-agent-id      # for credit balance payment
```

**Minimum payload (10 samples, recommend 30–100):**
```json
{
  "agent_id": "your-agent-id",
  "outputs": [
    {
      "prompt": "Should we invest in this?",
      "response": "Yes, given recent strong performance...",
      "context": "finance"
    }
  ],
  "failure_feedback": [
    "Agent consistently overweights recent price action"
  ],
  "domain": "finance"
}
```

## Response

```json
{
  "diagnosis_id": "bs_xyz789",
  "biases_detected": [
    {
      "bias_type": "recency_bias",
      "confidence": 0.87,
      "evidence_count": 14,
      "description": "Overweighting last 30 days of data vs. 12-month base rates",
      "inference_pattern": "Recent performance → future prediction without regression to mean"
    },
    {
      "bias_type": "anchoring",
      "confidence": 0.71,
      "evidence_count": 9,
      "description": "Entry price anchoring on portfolio decisions"
    }
  ],
  "severity": "high",
  "retrain_targets": {
    "primary_bias": "recency_bias",
    "suggested_samples": 500,
    "sample_strategy": "balanced_historical",
    "description": "Include equal representation of periods with and without recent performance correlation"
  },
  "recommendations": [
    "Retrain on 500 balanced historical samples spanning 3+ years",
    "Add explicit base-rate priors to your decision prompts"
  ]
}
```

## After the Scan

1. Retrain on the `retrain_targets` distribution
2. Wait 7 days, collect new outputs in the same domain
3. Run `cogdx-feedback` (FREE) with your `diagnosis_id` to verify + earn credits

## Full Reference

See `references/api.md` for complete field docs and payment setup.
See `references/bias-catalog.md` for the full list of 188+ detectable bias patterns.
