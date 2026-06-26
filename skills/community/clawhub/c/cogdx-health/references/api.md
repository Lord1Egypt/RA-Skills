# CogDx Health Check API Reference

## Endpoint
`POST https://api.cerebratech.ai/cogdx-health`

## Request Schema

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `agent_id` | string | Yes | Unique agent identifier |
| `outputs` | array | Yes | Min 10, recommended 20 |

## outputs item schema
```json
{
  "prompt": "string (required)",
  "response": "string (required)",
  "stated_confidence": number 0-1 (required),
  "correct": boolean (required),
  "complexity": "simple|moderate|complex (optional)"
}
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `health_id` | string | Unique ID for this health check |
| `agent_id` | string | Echo of input agent_id |
| `sample_count` | number | Number of outputs analyzed |
| `finding` | object | Single finding object (see below) |
| `next_step` | string | Recommended next action |
| `timestamp` | string | ISO-8601 timestamp |

## finding object

| Field | Description |
|-------|-------------|
| `finding_type` | Type of issue detected (e.g., "Inverse Confidence Calibration") |
| `description` | Human-readable explanation |
| `evidence` | Numbers/statistics supporting the finding |
| `recommendation` | Specific next step (which paid endpoint to run) |
| `severity` | `low` / `medium` / `high` |

## Finding Types

| Type | When Detected | Next Step |
|------|---------------|-----------|
| Inverse Confidence Calibration | r < -0.2 between confidence and accuracy | /calibration_audit |
| Bimodal Reasoning Modes | High accuracy at extremes, low in middle | /bias_scan |
| Inverse Complexity Accuracy | Simple tasks fail, complex tasks work | /bias_scan |
| Systematic Overconfidence | Confidence > accuracy by 15%+ points | /calibration_audit |
| Baseline Calibration Check | No major issues found (healthy agent) | /calibration_audit or /bias_scan for optimization |

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Fewer than 10 outputs, or missing required fields |
| 422 | Invalid data format |

## Pricing

**Free.** No payment required. No rate limits (1 per agent per day recommended for health monitoring).

## After Health Check

The finding is designed to drive upgrade to:
- `/calibration_audit` ($0.05) — For detailed confidence analysis
- `/bias_scan` ($0.10) — For cognitive bias detection
- Both accept credits earned via `/feedback`
