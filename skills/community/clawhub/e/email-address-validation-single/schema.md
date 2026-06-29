# Email Address Validation - Single Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `email-address-validation-single`

x402 availability: not enabled for this product.

## `verify`

Action slug: `verify`

Price: `5` credits

Verify a single email address for deliverability and validity. Performs syntax validation, DNS/MX record lookup, and SMTP-level mailbox verification without sending an email.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address_info` | `boolean` | no | Include additional address metadata such as free email provider detection and role account identification. Default: true. |
| `credits_info` | `boolean` | no | Include remaining credit balance in the response. Default: true. |
| `email` | `string` | yes | The email address to verify. |
| `timeout` | `integer` | no | Request timeout in seconds. Default: 10. |

Sample parameters:

```json
{
  "address_info": true,
  "credits_info": true,
  "email": "user@example.com",
  "timeout": 10
}
```

Generated JSON parameter schema:

```json
{
  "address_info": {
    "default": true,
    "description": "Include additional address metadata such as free email provider detection and role account identification. Default: true.",
    "required": false,
    "type": "boolean"
  },
  "credits_info": {
    "default": true,
    "description": "Include remaining credit balance in the response. Default: true.",
    "required": false,
    "type": "boolean"
  },
  "email": {
    "description": "The email address to verify.",
    "required": true,
    "type": "string"
  },
  "timeout": {
    "default": 10,
    "description": "Request timeout in seconds. Default: 10.",
    "maximum": 30,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```
