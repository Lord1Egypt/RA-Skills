# Larry config.json — Field Mapping from Onboarding Form

When generating a new client's config.json, map their onboarding answers to these fields.
Copy the structure from echo-system-1/config.json exactly — only update the values below.

## Field Mapping

### app section
```json
"app": {
  "name": "{client.business_name}",
  "description": "{client.product_description}",
  "audience": "{client.target_audience}",
  "problem": "Derive from product_description — what pain does their product solve?",
  "differentiator": "Derive from product_description — what makes their product unique?",
  "appStoreUrl": "Leave blank unless client provided a URL in notes",
  "category": "Infer from product_description (services/ecommerce/saas/creator/other)",
  "isMobileApp": false
}
```

### imageGen section
```json
"imageGen": {
  "provider": "openai",
  "model": "gpt-image-1.5",
  "basePrompt": "Generate from brand_voice + product category. See prompt patterns below.",
  "useBatchAPI": false,
  "apiKey": "__INJECTED_AT_RUNTIME__"
}
```

**basePrompt patterns by brand voice:**
- Bold/confident: "Bold graphic design, high contrast, strong typography shapes, portrait 1024x1536. No text."
- Educational/professional: "Clean infographic style, flat vector, muted blues and greys, portrait 1024x1536. No text."
- Casual/friendly: "Warm illustration style, soft colors, friendly characters, portrait 1024x1536. No text."
- Luxury/premium: "Minimalist luxury aesthetic, dark background, gold/cream accents, portrait 1024x1536. No text."
- Default (if unclear): "Flat vector illustration, minimalist design, portrait 1024x1536, muted color palette. No text."

### postiz section
```json
"postiz": {
  "apiKey": "__INJECTED_AT_RUNTIME__",
  "integrationIds": {
    "tiktok": "FILL_AFTER_OPERATOR_CONNECTS",
    "twitter": "FILL_AFTER_OPERATOR_CONNECTS"
  }
}
```
Leave integration IDs as "FILL_AFTER_OPERATOR_CONNECTS" — operator updates these after connecting in Postiz dashboard.

### posting section
```json
"posting": {
  "privacyLevel": "SELF_ONLY",
  "schedule": ["07:30"],
  "timezone": "Infer from client location if known, default America/New_York",
  "leadMinutes": 20,
  "hashtags": [
    "Generate 5 relevant hashtags from business_name + target_audience + product category"
  ],
  "crossPost": []
}
```
**privacyLevel starts as SELF_ONLY** — operator flips to PUBLIC after verifying test posts look correct.

## Hashtag Generation Rules
- 1 branded hashtag (e.g. #echoreviewsapp)
- 1 industry hashtag (e.g. #cleaningbusiness)
- 1 audience hashtag (e.g. #smallbusiness)
- 1 content type hashtag (e.g. #aitools or #automation)
- 1 broad reach hashtag (e.g. #entrepreneur or #founder)

## Complete Example (echo-system-1 as reference)
See: `~/Desktop/EVO_V2_VAULT/99-External-Systems/skills/larry/tiktok-marketing/systems/echo-system-1/config.json`
