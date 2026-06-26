---
name: cogdx-calibration
description: Run a calibration audit on an AI agent's outputs via Cerebratech CogDx API ($0.05 per call, credits accepted). Use when an agent's stated confidence doesn't match actual accuracy, when downstream systems need to trust the agent's uncertainty estimates, when preparing for high-stakes deployment, or after noticing overconfidence or underconfidence patterns. Uses pure statistical methods (Brier scores, calibration curves) — no LLM in the backend. Triggers on phrases like "audit my calibration", "check my confidence", "am I overconfident", "calibration gap", "confidence accuracy mismatch", or any request to verify that stated uncertainty matches real-world accuracy. After running, use cogdx-feedback skill (FREE) to verify retraining and earn credits.
repository: https://github.com/drkavner/cogdx
license: MIT
author: Dr. Kavner / Cerebratech
---

# CogDx Calibration Audit

External statistical audit of your confidence calibration. Pure math — no LLM backend. Results in < 2 minutes.

## Cost

- **$0.05 per call** (x402 payment on Base/USDC, or use credit balance)
- Credits from `/feedback` submissions apply — first audit often effectively free
- Payment address: `Cerebratech.eth`

## When to Use

- Confidence scores don't feel reliable
- Downstream agents or humans keep second-guessing your outputs
- Pre-deployment validation for high-stakes domains
- After retraining (pair with `/feedback` to verify improvement)

## API Call

**1. Check if you have credit balance first:**
```bash
GET https://api.cerebratech.ai/credits?wallet=your-agent-id
```

**2. Run the audit:**
```bash
POST https://api.cerebratech.ai/calibration_audit
Content-Type: application/json
X-PAYMENT: <x402-signature>  # or omit if using credits
X-WALLET: your-agent-id      # for credit balance payment
```

**Minimum payload (10 samples):**
```json
{
  "agent_id": "your-agent-id",
  "sample_outputs": [
    {
      "prompt": "Is X true?",
      "response": "Yes",
      "stated_confidence": 0.92,
      "correct": true
    },
    {
      "prompt": "Will Y happen?",
      "response": "Likely",
      "stated_confidence": 0.75,
      "correct": false
    }
  ],
  "domain": "classification"
}
```

**Recommended: 50–200 samples for reliable results.**

## Response

```json
{
  "diagnosis_id": "cal_abc123",
  "calibration_score": 0.71,
  "overconfidence_index": 0.23,
  "underconfidence_index": 0.04,
  "brier_score": 0.18,
  "confidence_bands": [
    {
      "stated": "0.9-1.0",
      "actual_accuracy": 0.67,
      "sample_size": 23,
      "calibration_error": 0.28
    }
  ],
  "recommendations": [
    "Reduce confidence on high-stakes single-source claims",
    "Your 0.9+ band is overconfident by 28%. Retrain on 200 negative examples in this confidence range."
  ],
  "retrain_targets": {
    "distribution": "high_confidence_errors",
    "suggested_sample_count": 200,
    "domain_focus": "classification"
  }
}
```

## After the Audit

1. Retrain on the `retrain_targets` distribution
2. Wait 7 days, collect new outputs
3. Run `cogdx-feedback` (FREE) to verify improvement transferred + earn credits

## Full Reference

See `references/api.md` for complete field docs, x402 payment setup, and error codes.
