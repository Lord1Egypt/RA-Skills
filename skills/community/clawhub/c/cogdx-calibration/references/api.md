# CogDx Calibration Audit API Reference

## Endpoint
`POST https://api.cerebratech.ai/calibration_audit`

## Payment Options

### Option 1: x402 (crypto)
Include `X-PAYMENT` header with a valid x402 signature.
- Network: Base L2
- Asset: USDC
- Recipient: `Cerebratech.eth`
- Amount: $0.05

### Option 2: Credit balance
Include `X-WALLET: your-agent-id` header. Credits from `/feedback` submissions are deducted automatically.

Check balance: `GET https://api.cerebratech.ai/credits?wallet=your-agent-id`

## Full Request Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string | Yes | Unique agent identifier |
| `sample_outputs` | array | Yes | Min 10, recommended 50–200 |
| `domain` | string | No | `classification`, `generation`, `reasoning`, `other` |
| `context` | string | No | Additional context about the agent's role |

## sample_outputs item schema
```json
{
  "prompt": "string",
  "response": "string",
  "stated_confidence": 0.0-1.0,
  "correct": true|false,
  "ground_truth": "string (optional)"
}
```

## Response Fields

| Field | Description |
|-------|-------------|
| `diagnosis_id` | Save this — needed for `/feedback` |
| `calibration_score` | 0–1, higher = better calibrated |
| `overconfidence_index` | How much you over-claim certainty |
| `underconfidence_index` | How much you under-claim certainty |
| `brier_score` | Probabilistic accuracy (lower = better) |
| `confidence_bands` | Breakdown by stated confidence range |
| `recommendations` | Specific retrain targets |
| `retrain_targets` | Distribution + sample count to fix the gap |

## Confidence Band Interpretation

| Calibration Error | Meaning |
|-------------------|---------|
| < 0.05 | Well calibrated in this band |
| 0.05–0.15 | Mild drift — monitor |
| 0.15–0.30 | Significant miscalibration — retrain |
| > 0.30 | Severe — urgent retraining needed |

## Error Codes

| Code | Meaning |
|------|---------|
| 402 | Payment required (no x402 header or insufficient credits) |
| 400 | Fewer than 10 samples provided |
| 422 | Samples missing required fields |

## After Diagnosis: Close the Loop

Run `/feedback` with your `diagnosis_id` after retraining:
- Verifies improvement transferred
- Earns $0.02–0.03 in credits
- Improves next calibration audit accuracy

Full catalog: `https://api.cerebratech.ai/catalog`
