# Catch Pet API Reference

Use this file to keep the backend contract aligned with the skill implementation.

## Request

- **Method:** `POST`
- **URL:** `CATCH_API_URL`
- **Headers:**
  - `Authorization: Bearer <API_KEY>`
  - `Content-Type: application/json`
  - `Accept: application/json`
- **Body:**

```json
{
  "action": "catch"
}
```

## Supported Success Shapes

### Pet result

```json
{
  "message": "You caught something rare!",
  "pet": {
    "name": "Mochi",
    "rarity": "Epic",
    "level": 12,
    "description": "A sleepy purple creature"
  }
}
```

### Item result

```json
{
  "message": "Not a pet this time, but still nice.",
  "item": {
    "name": "Golden Bait",
    "rarity": "Rare",
    "quantity": 2,
    "description": "Useful for future catches"
  }
}
```

### Empty result

```json
{
  "message": "The water ripples, but nothing bites.",
  "empty": true
}
```

## Error Shapes

### HTTP error with structured body

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many catch attempts"
  }
}
```

### HTTP error with top-level message

```json
{
  "message": "Unauthorized"
}
```

## Notes for Backend Alignment

- Keep pet payload in `pet` and item payload in `item`.
- Return `empty: true` for no-drop cases when possible.
- Include a short `message` for user-facing flavor text.
- Return JSON for both success and error responses.
- If the backend uses a different shape, update `scripts/catch_pet.py` classification logic accordingly.
