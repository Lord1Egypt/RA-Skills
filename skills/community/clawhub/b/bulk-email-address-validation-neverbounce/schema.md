# Bulk Email Address Validation - NeverBounce Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `bulk-email-address-validation-neverbounce`

x402 availability: not enabled for this product.

## `verify`

Action slug: `verify`

Price: `5` credits

Verify a list of email addresses in bulk (1-1000). Creates a verification job, polls for completion, and returns per-email results with summary statistics.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `emails` | `array` | yes | List of email addresses to verify in bulk (1-1000 emails). |
| `timeout` | `integer` | no | Maximum time to wait for job completion in seconds. Jobs may take longer for large lists. |

Sample parameters:

```json
{
  "emails": [
    "user@example.com"
  ],
  "timeout": 30
}
```

Generated JSON parameter schema:

```json
{
  "emails": {
    "description": "List of email addresses to verify in bulk (1-1000 emails).",
    "items": {
      "type": "string"
    },
    "maxItems": 1000,
    "minItems": 1,
    "required": true,
    "type": "array"
  },
  "timeout": {
    "default": 30,
    "description": "Maximum time to wait for job completion in seconds. Jobs may take longer for large lists.",
    "maximum": 300,
    "minimum": 10,
    "required": false,
    "type": "integer"
  }
}
```
