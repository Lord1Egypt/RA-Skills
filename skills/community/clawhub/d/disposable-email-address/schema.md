# Disposable Email Address Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `disposable-email-address`

x402 availability: not enabled for this product.

## `check`

Action slug: `check`

Price: `15` credits

Check the inbox of a previously created email address and retrieve all messages with full content including sender, subject, body, and received timestamp.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | `string` | yes | Email address to check. Must be an email address you previously created with the create action. Example: 'ai_agent_123@guerrillamail.com'. |

Sample parameters:

```json
{
  "email": "user@example.com"
}
```

Generated JSON parameter schema:

```json
{
  "email": {
    "description": "Email address to check. Must be an email address you previously created with the create action. Example: 'ai_agent_123@guerrillamail.com'.",
    "required": true,
    "type": "string"
  }
}
```

## `create`

Action slug: `create`

Price: `15` credits

Create a new temporary disposable email address with a 24-hour expiration. Returns the email address, creation time, and expiration time.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `username` | `string` | no | Preferred username for the email address. If not provided, a random username will be generated. Example: 'myagent' becomes 'myagent@guerrillamail.com'. |

Sample parameters:

```json
{
  "username": "example username"
}
```

Generated JSON parameter schema:

```json
{
  "username": {
    "description": "Preferred username for the email address. If not provided, a random username will be generated. Example: 'myagent' becomes 'myagent@guerrillamail.com'.",
    "required": false,
    "type": "string"
  }
}
```

## `fetch`

Action slug: `fetch`

Price: `15` credits

List all active (non-expired) email addresses belonging to the current user, along with creation time, expiration time, and hours remaining for each.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```
