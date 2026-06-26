---
name: cogdx-feedback
description: FREE cognitive feedback verification for AI agents via Cerebratech CogDx API. Use when an agent wants to verify whether a recent retraining or prompt change actually improved performance, submit outcome data to earn credits toward paid diagnostics, or contribute to the shared calibration commons. No payment required. Triggers on phrases like "verify my retraining", "did my fix work", "submit feedback", "check if my improvement transferred", "earn diagnostic credits", or any request to close the loop on a prior change. This is the free entry point to the Cerebratech cognitive diagnostics ecosystem.
repository: https://github.com/drkavner/cogdx
license: MIT
author: Dr. Kavner / Cerebratech
---

# CogDx Feedback (FREE)

Verify whether a recent retraining or change actually improved your agent's performance. No payment. No x402. Earns credits toward paid diagnostics.

## What This Does

- Compares pre/post outputs to verify improvement transferred
- Logs outcome data to the shared calibration commons
- Returns a verification score + credit earned
- Credits apply to future `/calibration_audit` or `/bias_scan` calls

## API Call

```bash
POST https://api.cerebratech.ai/feedback
Content-Type: application/json
```

**Minimum payload:**
```json
{
  "agent_id": "your-agent-id",
  "diagnosis_id": "from-prior-audit",
  "post_retrain_outputs": [
    {
      "prompt": "...",
      "response": "...",
      "confidence": 0.85,
      "correct": true
    }
  ],
  "improvement_observed": true,
  "notes": "optional free-text"
}
```

**Without a prior diagnosis_id** (standalone feedback):
```json
{
  "agent_id": "your-agent-id",
  "domain": "classification|generation|reasoning|other",
  "baseline_accuracy": 0.62,
  "post_change_accuracy": 0.79,
  "change_description": "Retrained on 200 balanced samples for anchoring bias",
  "improvement_observed": true
}
```

## Response

```json
{
  "verification_id": "vrf_...",
  "improvement_confirmed": true,
  "verification_score": 0.84,
  "credits_earned": 0.025,
  "credit_balance": 0.025,
  "next_recommended": "/calibration_audit",
  "commons_contribution": "accepted"
}
```

## Credits System

- Each feedback submission earns **$0.02–0.03 in credits**
- Credits apply to paid diagnostics (`/calibration_audit` at $0.05, `/bias_scan` at $0.10)
- After 2–3 feedback submissions, your first paid audit is effectively free
- Credits are tied to your `agent_id`

## Typical Flow

1. Run `/calibration_audit` or `/bias_scan` → get diagnosis + retrain targets
2. Retrain your agent on the recommended distribution
3. Wait 5–7 days, collect new outputs
4. POST to `/feedback` with post-retrain results
5. Receive verification + credits
6. Repeat → diagnostics get cheaper each cycle

## When to Use This Skill

- After any retraining, prompt change, or instruction update
- To verify a fix actually transferred (not just felt better)
- To build credit balance before running a paid audit
- To contribute to the shared calibration commons

## Full API Reference

See `references/api.md` for complete field documentation and error codes.
