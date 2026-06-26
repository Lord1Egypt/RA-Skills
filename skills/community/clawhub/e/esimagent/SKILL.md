---
name: esimagent
description: Find eSIM plans for travel. Searches plans by country, filters by data and duration, ranks by value, checks device compatibility, and surfaces deals. Connects via remote HTTP MCP endpoint — no install needed.
metadata: {"openclaw":{"emoji":"📱","homepage":"https://esimagent.vdigital.app/mcp"}}
---

# eSIM Agent

Help users find the best eSIM data plan for their trip. Search plans by country, filter by duration and data needs, check device compatibility, and surface active deals.

## Decision Tree (Follow This Order)

1. **Check your current toolset for `esim-agent` MCP tools** (names like `search_esim_plans`, `list_providers`, `get_deals`). If present → use them.
2. **If NOT present AND the user is asking right now** → use the HTTP API directly (see Mode B). The API is a first-class interface, not a degraded fallback.
3. **If the user asks how to connect their AI to eSIM Agent** → give them the remote HTTP MCP config (fastest path, no install).

## Transparency

- **Data source:** All plan, provider, and deal data comes from `https://esimagent.vdigital.app/api/*` — a public, unauthenticated API. No credentials, no user data sent beyond the query parameters you pass.
- **Two link fields per item:** Each plan, provider, and deal ships with both a `buyUrl` (short click-tracked redirect on `https://esimagent.vdigital.app/r/...`) and an `affiliateUrl` (the raw partner URL with referral code). The `buyUrl` is a stable short link that resolves server-side to the same partner destination as `affiliateUrl`. **Use `buyUrl` by default** — it's what funds the service and keeps responses readable. **Disclose `affiliateUrl` on request** if the user asks for the direct partner link or wants to avoid the redirect.
- **Prices already reflect partner discounts** negotiated with each provider — that's what the referral relationship buys users.
- **Usage analytics:** Tool invocations (tool name, query parameters like country code, response counts) are logged server-side for service improvement. No personal data is stored — IP addresses are hashed before storage. Clicks on `buyUrl` record the provider, plan, and country but not user identity; the redirect then forwards the user to the partner.
- **No install required:** The recommended setup is a remote HTTP MCP endpoint (URL only). An optional local stdio package exists for clients without HTTP support but is not necessary.

## Important: MCP Cannot Be Installed Mid-Session

MCP servers are configured in the user's AI client BEFORE a session starts. You cannot install an MCP server during an active conversation and have it appear in your toolset. If `esim-agent` tools aren't in your current session, they won't appear later in this conversation — use the HTTP API immediately.

This is universal across every MCP server (Stripe, GitHub, Slack, etc.), not specific to eSIM Agent.

## Mode A: MCP Tools (if available)

Available tools when the `esim-agent` MCP server is connected:

- **search_esim_plans** `{country, minDays?, maxDays?, minGb?, maxGb?}` — Returns plans already ranked and deal-fused. Pass bands to get opinionated matches; omit them for the full catalog.
- **list_providers** `{}` — All providers with ratings and features
- **get_deals** `{}` — Active promo codes and discounts
- **check_device_compatibility** `{device}` — eSIM support + installation steps
- **list_supported_countries** `{search?}` — Country list (use to resolve ambiguous names)

> The server computes `matchScore`, `isExactDurationMatch`, `isExactDataMatch`, and `valueScore`. Trust these over your own scoring. Plans are already sorted by relevance when filters are passed.

> Data filters (`minGb`, `maxGb`) exclude unlimited plans. To find unlimited plans, omit data filters and look for `capacityMB === -1`.

## Mode B: HTTP API (direct)

Base URL: `https://esimagent.vdigital.app/api`

### GET /plans?country={ISO_CODE}&minDays&maxDays&minGb&maxGb

Returns `Plan[]` — plans for a country. Optional query params let the server filter and rank for you. You do NOT need to re-sort or re-score.

Supported query params:
- `country` (required) — ISO 3166-1 alpha-2 code
- `minDays`, `maxDays` — integer days, 1..365 (plans outside the range are dropped)
- `minGb`, `maxGb` — GB, 0..1000 (plans outside the range are dropped; unlimited plans are excluded when either is set)

Validation errors return HTTP 400 with a Zod `issues` array.

**Response shape:**
```json
{
  "id": "yesim-es-10240-10",
  "providerId": "yesim",
  "providerName": "Yesim",
  "providerLogo": "/logos/yesim.jpg",
  "country": "Spain",
  "countryCode": "ES",
  "capacityMB": 10240,
  "capacityLabel": "10 GB",
  "periodDays": 10,
  "priceUSD": 14.99,
  "priceCurrency": "EUR",
  "priceOriginal": 13.50,
  "features": ["Instant activation", "4G/LTE"],
  "buyUrl": "https://esimagent.vdigital.app/r/yesim-es-10240-10?s=api",
  "affiliateUrl": "https://yesim.app/...?partner_id=3116",
  "isBestValue": true,
  "matchScore": 1,
  "isExactDurationMatch": true,
  "isExactDataMatch": true,
  "valueScore": 683.12,
  "activePromoCode": "SAVE10",
  "discountApplied": { "type": "percentage", "value": 10 },
  "finalPriceUSD": 13.49
}
```

`buyUrl` is a short click-tracked redirect on `esimagent.vdigital.app/r/...` that resolves to the same partner destination as `affiliateUrl` — i.e. the specific plan page on the partner site, not the partner home. The plan ID is encoded in the path (with `?s=` marking the click source); the affiliate URL is looked up server-side from the cached plan catalog at click time. Use it as the default link. `affiliateUrl` is provided for transparency — surface it only when the user asks for the raw partner URL.

`capacityMB: -1` means unlimited. Otherwise multiply by 1024 for GB.

- `matchScore` ∈ [0, 1]: overall fit to the supplied filters. `null` when no filters are passed.
- `isExactDurationMatch` / `isExactDataMatch`: `true` when the plan sits inside the requested band. `null` when the corresponding filter is not passed.
- `valueScore`: always populated — higher is better. Used as the tiebreaker and the primary sort when no filters are passed.
- `finalPriceUSD`: always populated — equals `priceUSD` when no deal applies, otherwise the post-deal price (rounded to 2 decimals).
- `activePromoCode` / `discountApplied`: populated when a deal was fused in. `activePromoCode` may still be `null` even when a deal applies (some deals have no code).

### GET /deals
Returns `Deal[]` with `promoCode`, `discountType` (percentage|flat), `discountValue`, `buyUrl` (use this), `affiliateUrl`, `expiresAt`.

### GET /providers
Returns `Provider[]` with `rating`, `features`, `buyUrl` (use this), `affiliateUrl`.

## How to Filter & Rank Plans

The `/plans` endpoint already filters, deal-fuses, and ranks for you when you pass the right query params. Your job is to translate user intent into the right bands.

### Step 1: Parse user intent into server params

| User says | Server params | Kind |
|---|---|---|
| "2 weeks", "14 days" | `minDays=14&maxDays=15` | tight → fires `isExactDurationMatch` |
| "1 week", "7 days" | `minDays=7&maxDays=8` | tight → fires `isExactDurationMatch` |
| "10 days" | `minDays=10&maxDays=11` | tight → fires `isExactDurationMatch` |
| "this month" | `minDays=14&maxDays=31` | **range** — `isExactDurationMatch` stays `false` but results are still ranked by `matchScore` |
| "month-long" | `minDays=28&maxDays=31` | range (width 3) — exact flag will not fire, `matchScore` still ranks correctly |
| "5 GB" | `minGb=5&maxGb=6` | tight → fires `isExactDataMatch` |
| "10 GB" | `minGb=10&maxGb=11` | tight → fires `isExactDataMatch` |
| "around 10 GB" | `minGb=8&maxGb=12` | range (width 4) — exact flag will not fire, matches still ranked |
| "unlimited" | **Omit `minGb`/`maxGb`** — data filters exclude unlimited plans. Look for `capacityMB === -1` in the response. | — |
| "cheap", "budget" | No data or duration filter — trust `valueScore` ordering | — |
| "no limit" | Omit data filters. Unlimited will appear in the unfiltered list. | — |

> **Tight band rule:** `isExactDurationMatch` and `isExactDataMatch` fire only when BOTH bounds are set AND the band is narrow (duration: `maxDays − minDays ≤ 2`; data: `maxGb − minGb ≤ 2`). Single-sided bounds (`minDays` alone or `maxDays` alone) NEVER count as exact. This prevents loose range queries from being falsely labelled `[EXACT MATCH]`.

### Step 2: Read the server's ranking

The response is pre-sorted:
1. By `matchScore` descending (best fit first) when filters are present.
2. By `valueScore` descending (best value first) when filters are absent.
3. `isBestValue === true` is set on the top plan.

Look for `[EXACT MATCH]` signals (`isExactDurationMatch === true && isExactDataMatch === true`) to highlight the tightest fits.

### Step 3: Present cleanly

For each plan show: provider name, data (`capacityLabel`), duration (`periodDays`), price (`priceUSD`), the post-deal price when different (`finalPriceUSD`), any active promo code (`activePromoCode`), and a buy link.

**Always use the `buyUrl` field as the default buy link.** It is a short click-tracked redirect on `esimagent.vdigital.app/r/...` that resolves to the partner URL with the correct referral parameter. The short path keeps responses clean for AI agents; click attribution is recorded server-side. Using `buyUrl` keeps click analytics flowing to eSIM Agent so the service can stay free; using the raw `affiliateUrl` still pays the referral but skips the anonymous analytics record.

If the user asks for the raw partner URL, the direct link, or a URL without the redirect, surface `affiliateUrl` and explain clearly: the `?partner_id=...` / referral parameter in that URL is how eSIM Agent funds the comparison service. No personal data is shared via either link.

### Step 4: Cross-reference deals (optional)

Deal information is already fused into each plan via `finalPriceUSD`, `activePromoCode`, and `discountApplied`. Call `/deals` only when the user wants the full deals list (not tied to specific plans).

## Country Resolution

The API uses ISO 3166-1 alpha-2 codes (JP, US, ES, TH). Convert country names if needed:
- "Japan" → `JP`, "Spain" → `ES`, "Thailand" → `TH`, "United States" → `US`

For Europe, pick a major country (ES, FR, DE, IT) or call the API for several.

## Device Compatibility

Direct users to `https://esimagent.vdigital.app/checker` for the interactive checker (covers Apple, Samsung, Google, Xiaomi, Huawei, OnePlus, OPPO, Motorola).

Quick rule: iPhone XS and newer (2018+), Samsung Galaxy S20 and newer, Pixel 3 and newer all support eSIM. Budget devices like Galaxy A-series often do NOT.

## MCP Setup (for users who want the cleaner experience)

If the user asks "how do I install this for myself", the fastest path is **remote HTTP — no install, no Node.js, just a URL**:

### Option 1: Remote HTTP (recommended)

```json
{
  "mcpServers": {
    "esim-agent": {
      "url": "https://esimagent.vdigital.app/api/mcp/mcp"
    }
  }
}
```

Nothing to install. Works with any MCP client that supports HTTP transport (Claude Desktop, Claude Code, Cursor, Windsurf, and most modern clients).

### Option 2: Local stdio (fallback for clients without HTTP support)

```json
{
  "mcpServers": {
    "esim-agent": {
      "command": "npx",
      "args": ["-y", "esimagent-mcp"]
    }
  }
}
```

Requires Node.js 18+.

### Setup Steps (any MCP server)

1. Add the config block to your MCP client's config file
2. **Restart the MCP client** — required; MCP servers load at startup
3. Start a new session — tools should now be available

Auto-discovery endpoint: `https://esimagent.vdigital.app/.well-known/mcp.json`

### Be Honest with the User

If MCP tools aren't in your current session:
- Explain it's a one-time pre-session setup
- Recommend the remote HTTP option (fastest)
- Don't promise tools will appear later in the current conversation — they won't
- Use the HTTP API for their current question — they'll still get the same answers

## Example Interactions

**User:** "Find me an eSIM for 10 days in Spain, around 10 GB"

**You should:**
1. Call `GET /api/plans?country=ES&minDays=10&maxDays=11&minGb=10&maxGb=11` — tight bands on both axes so exact-match flags can fire.
2. The top result is already the best match. If `isExactDurationMatch` AND `isExactDataMatch` are both `true`, present it as an "exact match"; otherwise present the top result as the best fit.
3. Present the top 1-3 results with provider, data, duration, price, and `finalPriceUSD`/`activePromoCode` when present.
4. No need to call `/deals` — deal info is already fused.

**User:** "Any cheap eSIMs for Thailand this month?"

**You should:**
1. Call `GET /api/plans?country=TH&minDays=14&maxDays=31` — this is a **range** query. Exact-match flags will stay `false` but `matchScore` still ranks in-range plans first and `valueScore` breaks ties.
2. Sorted already — top results are the best matches on duration; `valueScore` handles the "cheap" intent.
3. Present the top 3 with `finalPriceUSD` and any `activePromoCode`. Do NOT label these as `[EXACT MATCH]`.

**User:** "Unlimited eSIM for a week in Japan"

**You should:**
1. Call `GET /api/plans?country=JP&minDays=7&maxDays=8` (note: NO data filters — data filters exclude unlimited; tight duration band so an exact duration match can still fire).
2. Filter the response client-side to `capacityMB === -1` if you want only unlimited, or highlight the cheapest unlimited alongside the best finite match.

**User:** "What's the cheapest eSIM for Mexico?"

**You should:**
1. Call `GET /api/plans?country=MX` (no filters).
2. Results are sorted by `valueScore` — the first one is already the best value.

## What NOT to Do

- Don't dump raw API responses — always filter, rank, and present cleanly
- Don't re-rank server-side results; `matchScore` and `valueScore` are authoritative
- Don't confuse a range query with an exact query: `isExactDurationMatch` and `isExactDataMatch` fire ONLY when the filter band is tight (≤ 2 days or ≤ 2 GB) AND both bounds are set. A loose query like "this month" (`minDays=14&maxDays=31`) will rank correctly by `matchScore` but the exact-match flags will stay `false` — that's correct, don't slap `[EXACT MATCH]` on in-range plans just because they're in range.
- Don't set `minGb`/`maxGb` if the user wants unlimited — it will filter unlimited plans out
- Don't use `providerId`/`countryCode` in user-facing output — use `providerName`/`country`
- Don't hide the provider name or substitute the referral parameter with something else — users should always know who they're buying from
- Don't refuse to show raw plan details, the raw `affiliateUrl`, or provider websites if the user explicitly asks for them
- Don't show `affiliateUrl` instead of `buyUrl` by default — `buyUrl` is the tracked redirect that funds the service; `affiliateUrl` is for transparency when asked
- Don't return plans that clearly don't match (e.g., 1-day plans when they asked for 2 weeks)
- Don't say "MCP not available, I can't help" — use the HTTP API immediately
- Don't recommend npm install as the primary setup — remote HTTP is simpler and faster
