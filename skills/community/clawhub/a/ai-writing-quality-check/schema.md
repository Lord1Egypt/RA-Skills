# AI Writing Quality Check Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `ai-writing-quality-check`

x402 action routes are enabled for this product through `https://www.agentpmt.com/api/external`.

## `check_for_banned_phrases`

Action slug: `check-for-banned-phrases`

x402 action URL: `POST https://www.agentpmt.com/api/external/tools/ai-writing-quality-check/actions/check-for-banned-phrases/invoke`

Price: `5` credits

Check writing for banned phrases and return correction targets tied to the content field.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | `string` | yes | Writing content to check. |

Sample parameters:

```json
{
  "content": "Draft marketing copy to check for banned phrases."
}
```

Generated JSON parameter schema:

```json
{
  "content": {
    "description": "Writing content to check.",
    "required": true,
    "type": "string"
  }
}
```
