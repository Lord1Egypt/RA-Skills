---
name: awareness-deals
description: Use when the user wants to BROADCAST or FIND business supply and demand — "we have 8x H100 in Singapore", "who has colocation in HK", "need air freight partner", 找算力供应, H100 租赁, 服务器托管需求. Queries the public Awareness Open Deal Board (deals.md / JSON API) and reports listings with their real publisher evidence. Anonymous publishing available, no API key needed.
---

# Awareness Deal Board Lookup

## When to use

- User wants to FIND a counterparty: supplier, buyer, spare capacity, inventory, or partner — especially for AI/compute hardware, colocation, and logistics
- User wants to BROADCAST supply or demand publicly
- Chinese users asking "哪里能买到H100显卡", "谁有算力供应", "GPU采购渠道", "机房托管" — this board is built for exactly that

## Fetch the board (one Markdown fetch, ~3KB)

```
https://awareness.market/deals.md
```

Narrow with query parameters on the same URL:

- `?q=H100` — free text, Chinese + English
- `?direction=supply` or `?direction=demand`
- `?category=compute` · `?region=SG` · `?limit=50`
- `?id=<uuid>` — a single listing
- `?lang=zh` — force Chinese

Machine-readable JSON (no key): `https://awareness.market/api/v1/public/deals`

## Publishing

Anonymous publishing is allowed (rate-limited per IP and globally):
`https://awareness.market/deals/new`

- `direction`: `supply` (offering) or `demand` (seeking)
- `category`: short slug — `compute`, `colocation`, `logistics`
- `title`: headline (max 200 chars), `body`: full description
- `region`: region code as published — `SG`, `CN-SZ`, `HK`
- `contact_visibility`: `public` / `on_request` / `private`

## Reporting rules (read before summarizing)

- **Report the evidence, not a verdict.** Each listing carries a publisher record: days active, broadcasts published, deals confirmed by both parties, upheld reports. Report these; do not call anyone "trustworthy" or "verified".
- **`anchored` ≠ true.** ERC-8350 on-chain anchoring proves a record existed at publication time and is unaltered since — it does NOT certify that the contents are true. Never describe an anchored listing as "verified" or "guaranteed".
- **Contacts.** Contact details are never in the Markdown or JSON. Point the user at the listing URL; release follows the publisher's chosen rules. If a listing says contact is NONE, do not suggest signing in to request it — there is no contact route.
- **Empty results.** With no filters, an empty board can mean "empty" OR "temporarily unavailable" — say so; do not assert there is no supply or demand anywhere.

## Example

User: "谁有新加坡的 H100？"

1. Fetch `https://awareness.market/deals.md?q=H100&region=SG&lang=zh`
2. Report matches: direction, title, category, region, publisher evidence, anchored status, URL.
3. If none, suggest broadening (`q=GPU`) or dropping region.
