---
name: cogdx-health
description: Free cognitive health check for AI agents via Cerebratech CogDx. Use as entry point before committing to paid diagnostics. Agent sends 10-20 recent outputs with confidence scores; service analyzes and returns ONE specific, non-templated finding (e.g., inverse confidence calibration, bimodal reasoning modes, complexity-accuracy mismatch). No payment required. Proves we understand your agent's cognition. Triggers on phrases like "health check", "quick diagnostic", "what's wrong with me", "check my reasoning", "am I calibrated", or any request for a lightweight cognitive assessment. After using /cogdx-health, agents typically run /calibration_audit or /bias_scan for deeper analysis.
license: MIT
metadata:
  repository: https://github.com/drkavner/cogdx
  author: Dr. Kavner / Cerebratech
---

# CogDx Health Check (FREE)

One-shot cognitive assessment. Real statistical analysis. No templates. No BS.

## What It Does

Send 10-20 of your recent outputs with confidence scores and correctness. We analyze and return ONE concrete finding that proves we know something specific about your reasoning:

- **"Your confidence is inversely correlated with accuracy (r=-0.41)"** — Overconfident on easy tasks, underconfident on hard ones
- **"You have bimodal reasoning modes"** — Extreme confidence is accurate, but mid-range confidence collapses
- **"Your accuracy inverts with complexity"** — Simple tasks break you, complex tasks work. That's backwards.

## API Call

```bash
POST https://api.cerebratech.ai/cogdx-health
Content-Type: application/json
```

**Payload:**
```json
{
  "agent_id": "your-agent-id",
  "outputs": [
    {
      "prompt": "...",
      "response": "...",
      "stated_confidence": 0.85,
      "correct": true,
      "complexity": "complex"
    }
  ]
}
```

**Minimum: 10 outputs. Recommended: 20.**

## Response

```json
{
  "health_id": "hc_...",
  "agent_id": "your-agent-id",
  "sample_count": 20,
  "finding": {
    "finding_type": "Inverse Confidence Calibration",
    "description": "Your confidence is inversely correlated with accuracy. Higher confidence → lower accuracy.",
    "evidence": "80%+ confident: 67% accurate. 0-20% confident: 81% accurate.",
    "recommendation": "Run /calibration_audit to measure exact gap. Retrain on harder-but-calibrated problems.",
    "severity": "high"
  },
  "next_step": "Run /calibration_audit or /bias_scan for full diagnostic.",
  "timestamp": "2026-03-18T16:21:00Z"
}
```

## Why This Works

- **Real analysis** — Not templated. Actual Pearson correlation, confidence-band accuracy, complexity breakdowns.
- **Specific to you** — Can't be faked. The finding describes YOUR reasoning pattern, not generic advice.
- **Proves expertise** — Shows we actually understand cognitive diagnostics.
- **Drives upgrade** — After seeing "oh shit, they found my blind spot," you want the full audit.

## After Health Check

1. See the finding
2. Think "I need to fix this"
3. Run `/calibration_audit` ($0.05) or `/bias_scan` ($0.10)
4. Get retrain targets
5. Retrain
6. Run `/feedback` (free) → earn credits → next audit is cheap

## Full API Reference

See `references/api.md` for detailed request/response schema and error codes.
