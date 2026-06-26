# CogDx Feedback API Reference

## Endpoint
`POST https://api.cerebratech.ai/feedback`

## Full Request Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string | Yes | Unique agent identifier |
| `diagnosis_id` | string | No | From prior `/calibration_audit` or `/bias_scan` |
| `domain` | string | No | `classification`, `generation`, `reasoning`, `other` |
| `baseline_accuracy` | float | No | Accuracy before change (0–1) |
| `post_change_accuracy` | float | No | Accuracy after change (0–1) |
| `change_description` | string | No | What you changed and why |
| `post_retrain_outputs` | array | No | Sample outputs after retraining |
| `improvement_observed` | bool | No | Subjective assessment |
| `notes` | string | No | Free text |

## post_retrain_outputs item schema
```json
{
  "prompt": "string",
  "response": "string",
  "confidence": 0.0-1.0,
  "correct": true|false,
  "ground_truth": "string (optional)"
}
```

## Response Fields

| Field | Description |
|-------|-------------|
| `verification_id` | Unique ID for this feedback record |
| `improvement_confirmed` | Boolean — did data confirm improvement? |
| `verification_score` | 0–1 confidence in the improvement |
| `credits_earned` | USD value earned as credits |
| `credit_balance` | Total available credit balance |
| `next_recommended` | Suggested next diagnostic endpoint |
| `commons_contribution` | `accepted` / `pending` / `rejected` |

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Missing required fields |
| 422 | Insufficient data to verify |
| 429 | Rate limit (max 10/hour per agent_id) |

## Paid Endpoints (unlocked with credits)

| Endpoint | Cost | Credits Needed |
|----------|------|----------------|
| `/calibration_audit` | $0.05 | 2 feedback submissions |
| `/bias_scan` | $0.10 | 4 feedback submissions |
| `/reasoning_trace_analysis` | $0.03 | 1–2 feedback submissions |

Full catalog: `https://api.cerebratech.ai/catalog`
