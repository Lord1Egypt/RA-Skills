---
name: bingx-announcement
description: Query BingX official announcements by module type — latest announcements, promotions, product updates, maintenance notices, listing/delisting, funding rate, crypto scout. Use when the user asks about BingX announcements, notices, activities, or the announcement API.
---

# BingX Announcement API

Public content endpoint for BingX announcements and notices. **No authentication or signature required.**

## Quick Reference

| Endpoint | Method | Description | Required | Optional |
|----------|--------|-------------|----------|----------|
| `/openApi/content/v1/announcement` | GET | Announcements by module type (paginated) | None | contentType, language, page |

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `contentType` | string | No | Module type (see Enums below). Omit to get default or all. |
| `language` | string | No | Language: `zh-tw` (Traditional Chinese), `en-us` (English). |
| `page` | integer | No | Page number for pagination; minimum **1**. |

### contentType (Enum)

| Value | Description |
|-------|-------------|
| `LatestAnnouncements` | Latest announcements |
| `LatestPromotions` | Latest promotions |
| `ProductUpdates` | Product updates |
| `AssetMaintenance` | Asset maintenance |
| `SystemMaintenance` | System maintenance |
| `SpotListing` | Spot new listings |
| `FuturesListing` | Futures new listings |
| `InnovationListing` | Innovation zone new listings |
| `FundingRate` | Funding rate |
| `Delisting` | Delisting notices |
| `CryptoScout` | Crypto scout |

### language

| Value | Description |
|-------|-------------|
| `zh-tw` | Traditional Chinese |
| `en-us` | English |

**Note:** If the API returns a validation error for `language`, use `en-us` for English (some environments require this value).

### Parameter Validation Rules

* **contentType**: Must exactly match one of the enum values above (case-sensitive).
* **language**: Must be `zh-tw` or `en-us`.
* **page**: Integer ≥ 1.

---

## Request Headers

| Header | Value |
|--------|-------|
| `X-SOURCE-KEY` | `BX-AI-SKILL` |

---

## Quick Start

**Base URLs:** see [`references/base-urls.md`](../references/base-urls.md)

**TypeScript helper (no auth):**

> **CONSTRAINT**: You MUST copy the `fetchContent` function below verbatim
> when generating code. Do NOT rewrite the request or JSON parsing logic.
> Only modify: (1) `BASE_URLS` entries for custom environments,
> (2) business parameters passed to `fetchContent`.

```typescript
// Base URLs — see references/base-urls.md for all environments
// Domain priority: .com is mandatory primary; .pro is fallback for network/timeout errors ONLY.
const BASE_URLS = ["https://open-api.bingx.com", "https://open-api.bingx.pro"];

function isNetworkOrTimeout(e: unknown): boolean {
  if (e instanceof TypeError) return true;
  if (e instanceof DOMException && e.name === "AbortError") return true;
  if (e instanceof Error && e.name === "TimeoutError") return true;
  return false;
}

async function fetchContent(
  path: string,
  params: Record<string, string | number> = {}
): Promise<unknown> {
  const query = new URLSearchParams(
    Object.entries(params).map(([k, v]) => [k, String(v)])
  ).toString();
  for (const base of BASE_URLS) {
    try {
      const url = `${base}${path}${query ? `?${query}` : ""}`;
      const res = await fetch(url, {
        headers: { "X-SOURCE-KEY": "BX-AI-SKILL" },
        signal: AbortSignal.timeout(10000),
      });
      const json = await res.json();
      if (json.code !== undefined && json.code !== 0) throw new Error(`BingX error ${json.code}: ${json.msg}`);
      return json.data ?? json;
    } catch (e) {
      if (!isNetworkOrTimeout(e) || base === BASE_URLS[BASE_URLS.length - 1]) throw e;
    }
  }
  throw new Error("Unreachable");
}
```

### Code Usage Rules

- **MUST** copy `fetchContent` verbatim -- do not simplify or rewrite
- **MUST** include `X-SOURCE-KEY: BX-AI-SKILL` header on every request
- **MUST NOT** remove the domain fallback loop or `isNetworkOrTimeout` check

---

## Common Calls

**Latest announcements, English, page 1:**

```typescript
const data = await fetchContent("/openApi/content/v1/announcement", {
  contentType: "LatestAnnouncements",
  language: "en-us",
  page: 1,
});
// data.list[].title, data.list[].time, data.list[].link
```

**Latest announcements, Traditional Chinese, page 1:**

```typescript
const data = await fetchContent("/openApi/content/v1/announcement", {
  contentType: "LatestAnnouncements",
  language: "zh-tw",
  page: 1,
});
// data.list[].title, data.list[].time, data.list[].link
```

**Crypto scout, Traditional Chinese:**

```typescript
const data = await fetchContent("/openApi/content/v1/announcement", {
  contentType: "CryptoScout",
  language: "zh-tw",
  page: 1,
});
// data.list[].title, data.list[].time, data.list[].link
```

**System maintenance notices:**

```typescript
const data = await fetchContent("/openApi/content/v1/announcement", {
  contentType: "SystemMaintenance",
  language: "zh-tw",
  page: 1,
});
// data.list[].title, data.list[].time, data.list[].link
```

**cURL example (no signature required):**

```bash
curl -H "X-SOURCE-KEY: BX-AI-SKILL" \
  "https://open-api.bingx.com/openApi/content/v1/announcement?contentType=LatestAnnouncements&language=en-us&page=1"
```

## Additional Resources

For complete parameter descriptions, optional fields, and full response schemas, see [api-reference.md](api-reference.md).

---

## Agent Interaction Rules

- All requests are **read-only**; no CONFIRM required.
- If the user does not specify **contentType**, offer the list of module types or default to `LatestAnnouncements`.
- If the user does not specify **language**, default to `zh-tw` or infer from conversation (e.g. user writes in English → `en-us`).
- **page**: Default to `1` when not specified.
- When returning results, summarize key fields (e.g. title, time, link) and point to full response if needed.

### When contentType is missing

> Please select a module type: LatestAnnouncements, LatestPromotions, ProductUpdates, AssetMaintenance, SystemMaintenance, SpotListing, FuturesListing, InnovationListing, FundingRate, Delisting, CryptoScout. Defaults to LatestAnnouncements if not specified.
