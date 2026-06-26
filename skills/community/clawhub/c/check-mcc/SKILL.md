---
name: check-mcc
description: >
  Look up credit card rewards eligibility for merchants. Find the best credit card
  to use at any store, restaurant, or online merchant by checking MCC codes and
  card bonus categories. Use when the user asks which card to use, what rewards
  they'll earn, or wants to look up a merchant's MCC code.
version: 1.0.0
triggers:
  - "which card should I use at {merchant}"
  - "what card to use at {merchant}"
  - "best card for {merchant}"
  - "check mcc for {merchant}"
  - "mcc code for {merchant}"
  - "what rewards at {merchant}"
  - "card rewards at {merchant}"
  - "check-mcc lookup {domain}"
  - "check-mcc search {query}"
  - "check-mcc cards {mcc}"
tools:
  - http
author: gibtang
tags: [finance, credit-cards, rewards, mcc, travel-hacking]
config:
  baseUrl:
    type: string
    default: "https://check-mcc.com"
    description: "Base URL for the CheckMCC API"
  defaultRegion:
    type: string
    default: "US"
    description: "Default region for card eligibility (SG or US)"
---

# CheckMCC Skill

Look up credit card rewards eligibility for any merchant. Returns which cards earn bonus rewards at a given store based on its MCC (Merchant Category Code).

## Base URL

All API calls go to the configured `baseUrl` (default: `https://check-mcc.com`).

## Commands

### 1. Lookup by Domain (`check-mcc lookup`)

Look up a merchant by its website domain. Returns MCC code, category, and eligible cards.

**When to use:** User mentions a website or online store (e.g., "shopee.sg", "amazon.com").

```
GET {baseUrl}/api/store-by-domain?domain={domain}&region={region}
```

**Parameters:**
- `domain` (required) — The merchant's domain (e.g., `amazon.com`, `shopee.sg`). Protocol, www, and paths are auto-stripped.
- `region` (optional) — `SG` (Singapore) or `US` (United States). Defaults to `SG` if omitted.

**Response:**
```json
{
  "id": "...",
  "Store": "Amazon",
  "MCC": "5912",
  "Country": "US",
  "Category": "Drug Stores and Pharmacies",
  "type": "online",
  "url": "https://amazon.com",
  "eligibleCards": [
    {
      "name": "Citi Rewards Card",
      "shortName": "CRMC",
      "eligible": true,
      "reason": "4 mpd on online spend",
      "mpd": "4",
      "spendCap": "$1,000/month"
    },
    {
      "name": "DBS Woman's World Card",
      "shortName": "WWMC",
      "eligible": false,
      "reason": "Excluded: insurance and hospitals"
    }
  ]
}
```

**On 404:** The merchant is not in the database. Suggest the user submit it via the website.

### 2. Search by Name (`check-mcc search`)

Search for merchants by name. Returns matching store names and their MCC codes.

**When to use:** User names a store but doesn't provide a domain (e.g., "Starbucks", "NTUC FairPrice").

```
GET {baseUrl}/api/merchants/search?q={query}
```

**Parameters:**
- `q` (required) — Search query. Case-insensitive partial match.

**Response:**
```json
{
  "merchants": [
    { "Store": "Starbucks", "MCC": 5814 },
    { "Store": "Starbucks Coffee", "MCC": 5814 }
  ],
  "userDisabledCards": null
}
```

If multiple results are found, present them to the user and ask which one they mean. If a single clear match is found, proceed to look up card eligibility using the MCC code.

### 3. Card Eligibility by MCC (`check-mcc cards`)

Get card eligibility for a specific MCC code. Use when you already know the MCC (e.g., from a search result or the user provided it directly).

**When to use:** User asks about cards for a known MCC code (e.g., "what cards for MCC 5814?") or after getting MCC from a search.

```
GET {baseUrl}/api/store-by-domain?domain=_mcc_{mcc}&region={region}
```

Alternatively, if you have a merchant name, search first and then use the domain lookup for full card details.

### 4. Validate MCC Code

Check if an MCC code is valid.

```
GET {baseUrl}/api/mcc/codes
```

**Response:**
```json
{
  "codes": ["0001", "0002", ..., "9999"]
}
```

Use this to validate a user-provided MCC before looking up cards.

## Workflow

Follow this decision tree when a user asks about card rewards:

1. **User provides a domain/URL** → Use `lookup` directly
2. **User provides a store name** → Use `search` to find the merchant, then `lookup` on the matching domain for card details
3. **User provides an MCC code** → Validate with `codes` endpoint, then explain the category and card eligibility
4. **Ambiguous result** → Show the user the options and ask them to clarify

## Presenting Results

When showing card eligibility to the user:

1. **Lead with eligible cards** — These earn bonus rewards at this merchant
2. **Format clearly:**
   ```
   Best cards for {Store} (MCC {code} - {Category}):

   ✅ Citi Rewards Card — 4 mpd on online spend (cap: $1,000/month)
   ✅ UOB PPV — 4 mpd on mobile contactless payments

   ❌ DBS Woman's World Card — Excluded: insurance and hospitals
   ```
3. **Include the MCC code and category** so the user understands why certain cards qualify
4. **Note spend caps and special conditions** when present in the response

## Region Handling

- The API supports `region=SG` (Singapore) and `region=US` (United States)
- Different regions return different card eligibility lists (different card portfolios)
- If the user doesn't specify a region, use the configured `defaultRegion`
- SG cards: DBS, UOB, OCBC, HSBC, Citi Singapore
- US cards: Chase, Amex, Citi US, Capital One, etc.

## Error Handling

- **404 on lookup:** Merchant not found. Tell the user: "This merchant isn't in our database yet. You can submit it at check-mcc.com"
- **400 on lookup:** Invalid domain format. Ask the user to provide a valid domain
- **Empty search results:** No merchants match. Suggest trying a different name or partial name
- **API errors (5xx):** Temporary issue. Suggest trying again later

## Examples

**User:** "Which card should I use at Shopee?"
**You:** Search for "Shopee" → find `shopee.sg` → lookup domain → show eligible cards

**User:** "Best card for Amazon?"
**You:** Lookup `amazon.com` → show eligible cards for the user's region

**User:** "What's the MCC code for restaurants?"
**You:** Explain MCC 5812 (Eating Places) and 5814 (Fast Food), then offer to look up card eligibility

**User:** "check-mcc lookup godaddy.com"
**You:** Directly call lookup with `domain=godaddy.com` → show results
