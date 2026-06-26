# Azure AI Foundry FLUX API Reference

## Endpoint Format

```
POST https://<resource>.services.ai.azure.com/providers/blackforestlabs/v1/flux-2-pro?api-version=preview
```

## Authentication

```
Authorization: Bearer YOUR_KEY_HERE
```

## Request Body

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| prompt | string | ✅ | — | Text description of desired image |
| width | int | ❌ | 1024 | Image width (256–1440, multiple of 32) |
| height | int | ❌ | 1024 | Image height (256–1440, multiple of 32) |
| n | int | ✅ | — | Number of images (must be 1) |
| model | string | ✅ | — | Must be `"FLUX.2-pro"` |
| seed | int | ❌ | random | Reproducibility seed |

**Critical:** `n` and `model` are required. Omitting them returns HTTP 500.

## Response

```json
{
  "data": [
    {
      "b64_json": "<base64-encoded PNG>",
      "revised_prompt": "...",
      "content_filter_results": { ... }
    }
  ]
}
```

## Limitations

- One image per request (`n: 1` only)
- ~30–120 seconds per generation
- Content filter may reject prompts (returns 400)
- Chinese text rendering not supported — use Canvas overlay
- Serialize requests; parallel calls may cause instability

## Common Sizes

| Use Case | Width | Height |
|----------|-------|--------|
| Square | 1024 | 1024 |
| Landscape 16:9 | 1440 | 816 |
| Portrait 9:16 | 816 | 1440 |
| A3 print poster | 1240 | 1754 |
