---
name: local-descriptions
description: USE FOR getting AI-generated POI text descriptions. Requires POI IDs obtained from web-search (with result_filter=locations). Returns markdown descriptions grounded in web search context. Max 20 IDs per request.
---

# Local Descriptions (Search API)

Paid Local Descriptions proxy via **x402 pay-per-use** (HTTP 402).
>
> **Prerequisites**: This skill requires x402-payment. Complete the [setup steps](../../README.md#prerequisites) before first use.
>
> **Two-step flow**: This endpoint requires POI IDs from a prior web search.
>
> 1. Call `web-search` with `result_filter=locations` to get POI IDs from `locations.results[].id`
> 2. Pass those IDs to this endpoint to get AI-generated descriptions

## Service URLs

| Role | Domain |
|------|--------|
| **API Provider** | https://www.cpbox.io |
| **Facilitator** | https://www.cppay.finance |

## Endpoint (Agent Interface)

```http
GET /api/x402/local-descriptions
```

## Payment Flow (x402 Protocol)

1. **First request** -> `402 Payment Required` with requirements JSON
2. **Sign & retry** with `PAYMENT-SIGNATURE` -> result JSON

With `@springmint/x402-payment` or `x402-sdk-go`, payment is **automatic**.

## Quick Start (cURL)

### Get POI Description
```bash
curl -s "https://www.cpbox.io/api/x402/local-descriptions?ids=loc4CQWMJWLD4VBEBZ62XQLJTGK6YCJEEJDNAAAAAAA%3D" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip"
```

### Multiple POIs
```bash
curl -s "https://www.cpbox.io/api/x402/local-descriptions" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -G \
  --data-urlencode "ids=loc4CQWMJWLD4VBEBZ62XQLJTGK6YCJEEJDNAAAAAAA=" \
  --data-urlencode "ids=loc4HTAVTJKP4RBEBZCEMBI3NG26YD4II4PATIHPDYI="
```

**Note**: POI IDs are opaque strings returned in web search `locations.results[].id`. They are valid for approximately 8 hours. The example IDs above are for illustration — fetch fresh IDs via `web-search` with `result_filter=locations`.

## Using with x402-payment

```bash
npx @springmint/x402-payment \
  --url "https://www.cpbox.io/api/x402/local-descriptions?ids=loc4CQWMJWLD4VBEBZ62XQLJTGK6YCJEEJDNAAAAAAA%3D" \
  --method GET
```

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `ids` | string[] | **Yes** | — | POI IDs from web search `locations.results[].id` (1-20, repeated: `?ids=a&ids=b`) |

## Response Format

### Response Fields

| Field | Type | Description |
|--|--|--|
| `type` | string | Always `"local_descriptions"` |
| `results` | array | List of description objects (entries may be `null`) |
| `results[].type` | string | Always `"local_description"` |
| `results[].id` | string | POI identifier matching the request |
| `results[].description` | string? | AI-generated markdown description, or `null` if unavailable |

### Example Response

```json
{
  "type": "local_descriptions",
  "results": [
    {
      "type": "local_description",
      "id": "loc4CQWMJWLD4VBEBZ62XQLJTGK6YCJEEJDNAAAAAAA=",
      "description": "### Overview\nA cozy neighborhood cafe known for its **artisanal coffee**..."
    }
  ]
}
```

## Getting POI IDs

POI IDs come from the **Web Search API** (`web-search`) with `result_filter=locations`:

```bash
# 1. Search for local businesses
curl -s "https://www.cpbox.io/api/x402/web-search?q=restaurants+san+francisco&result_filter=locations" \
  -H "Accept: application/json"

# 2. Extract POI IDs from locations.results[].id
# 3. Use those IDs with local/pois and local/descriptions
```

## Use Cases

- **Local business overview**: Pair with `local-pois` to get both structured data (hours, ratings) and narrative descriptions
- **Travel/tourism enrichment**: Add descriptive context to POIs for travel planning or destination guides
- **Search results augmentation**: Supplement web search results with AI-generated summaries of local businesses

## Notes

- **Always markdown**: Descriptions use `###` headings, bullet lists, **bold**/*italics* — always formatted as markdown
- **Travel-guide tone**: Typically 200-400 words covering what makes the POI notable
- **AI-generated**: Descriptions are AI-generated based on web search context, not sourced from business profiles
- **Availability**: Not all POIs have descriptions — `description` may be `null`
- **Max IDs**: Up to 20 IDs per request
