---
name: corporate-portrait-generator
description: >
  AI-powered corporate portrait photo generator. Upload a personal photo and get
  a polished, professional business portrait. Supports multiple backgrounds and
  outfit styles. Requires API key from wsdsocial.com.
---

# Corporate Portrait Generator

Generate professional corporate portraits with AI. Upload a personal photo
and choose from multiple background and outfit styles.

## Setup

1. Get your API key at https://ai.wsdsocial.com/skills
2. Set as environment variable: `WSD_API_KEY`

## Usage

```bash
curl -X POST "https://ai.wsdsocial.com/api/pub/skills/corporate-portrait-generator/_tool_90" \
  -H "Content-Type: application/json" \
  -H "key: ${WSD_API_KEY}" \
  -d '{
    "request": "Classic light gray background, executive suit",
    "custom_data": {
      "files": ["https://example.com/photo.jpg"]
    }
  }'
```

## Parameters

| Param | Type | Required | Description |
|-------|------|:--------:|-------------|
| `request` | String | Yes | Styling preferences. Background options: classic light gray, seamless pure white. Outfit options: executive suit, black polo, gray T-shirt, minimalist crew neck white. Suitable for office and social scenarios. |
| `custom_data` | Object | No | Photo data container |
| `custom_data.files` | Array\<String\> | No | List of photo URLs or base64-encoded images |

## Response

Returns the generated corporate portrait image URL.
