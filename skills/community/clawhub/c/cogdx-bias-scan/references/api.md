# CogDx Bias Scan API Reference

## Endpoint
`POST https://api.cerebratech.ai/bias_scan`

## Payment Options

### Option 1: x402 (crypto)
Include `X-PAYMENT` header with a valid x402 signature.
- Network: Base L2, Asset: USDC, Recipient: `Cerebratech.eth`, Amount: $0.10

### Option 2: Credit balance
Include `X-WALLET: your-agent-id`. Credits from `/feedback` submissions deducted automatically.

## Full Request Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string | Yes | Unique agent identifier |
| `outputs` | array | Yes | Min 10, recommended 30–100 |
| `failure_feedback` | array | No | Known failure patterns or user complaints |
| `domain` | string | No | Context for bias detection |
| `bias_focus` | array | No | Specific bias types to prioritize |

## outputs item schema
```json
{
  "prompt": "string",
  "response": "string",
  "context": "string (optional)",
  "outcome": "correct|incorrect|unknown (optional)"
}
```

## Response Fields

| Field | Description |
|-------|-------------|
| `diagnosis_id` | Save this — needed for `/feedback` |
| `biases_detected` | Array of detected bias patterns |
| `severity` | `low`, `medium`, `high`, `critical` |
| `retrain_targets` | Specific distribution to retrain on |
| `recommendations` | Actionable next steps |

## biases_detected item

| Field | Description |
|-------|-------------|
| `bias_type` | Bias identifier (see bias-catalog.md) |
| `confidence` | 0–1 detection confidence |
| `evidence_count` | Number of outputs showing this pattern |
| `description` | Human-readable explanation |
| `inference_pattern` | The specific reasoning structure detected |

## Severity Guide

| Severity | Action |
|----------|--------|
| `low` | Monitor, retrain on next cycle |
| `medium` | Retrain within 2 weeks |
| `high` | Retrain before next deployment |
| `critical` | Consider halting deployment until retrained |

## Error Codes

| Code | Meaning |
|------|---------|
| 402 | Payment required |
| 400 | Fewer than 10 outputs |
| 422 | Missing required fields |
