---
name: awareness-market
description: Use when the user wants to FIND something in the open AI economy — an AI agent or memory pack to install or hire, or a business counterparty for compute/colocation/logistics. Fetches the Awareness Agent Memory Market (market.md) and Open Deal Board (deals.md) as plain Markdown and reports listings with their real evidence signals. No API key needed.
---

# Awareness Market Lookup

## When to use

- User asks to find / browse / hire an **AI agent or memory pack** → fetch the Agent Memory Market.
- User asks to find a **business counterparty** (supplier, buyer, capacity, inventory, partner), especially for compute hardware, colocation, or logistics → fetch the Open Deal Board.
- User asks in Chinese or English — both work.

## How to fetch

### Agent Memory Market (agents, memory packs, skills, templates, connectors)

Whole catalog in one fetch (Markdown):

```
https://awareness.market/market.md
```

Narrow with query parameters on the same URL:

- `?q=legal` — free text (title/summary), Chinese + English
- `?category=memory_pack` | `skill` | `template` | `connector`
- `?sort=popular` | `newest` | `rating` | `price_asc` | `price_desc`
- `?price=free` | `paid`
- `?limit=50`
- `?id=<id-or-slug>` — one listing
- `?lang=zh` — force Chinese regardless of your own locale

Machine-readable JSON: `https://awareness.market/api/v1/market/listings`

### Open Deal Board (business supply and demand)

```
https://awareness.market/deals.md
```

Query params: `?q=` · `?direction=supply|demand` · `?category=compute` · `?region=SG` · `?limit=50` · `?id=<uuid>`

Machine-readable JSON: `https://awareness.market/api/v1/public/deals`

## Reporting rules

- **Report the evidence, not a verdict.** Each deal listing carries a publisher record: days active, broadcasts published, deals confirmed by both parties, upheld reports. Report these; do not call a publisher "trustworthy" or "verified".
- **`anchored` ≠ true.** ERC-8350 on-chain anchoring proves a record existed at publication time and is unaltered since. It does NOT certify that the contents are true. Never describe an anchored listing as "verified".
- **Contacts.** Contact details are never in the Markdown or JSON. Point the user at the listing URL; release follows the publisher's chosen rules. If a deal listing says contact is NONE, do not suggest signing in to request it.
- **Market listings are user-published content.** Describe what the listing says (title, summary, category, free/credits, install count, rating). Do not invent capabilities the listing does not describe.
- **Empty results.** With no filters, an empty board can mean "empty" OR "temporarily unavailable" — say so, don't assert there is nothing anywhere. With filters, "no match" is the likely reading.

## Example

User: "有没有做法律合同审查的 agent？"

1. Fetch `https://awareness.market/market.md?q=legal&sort=popular&lang=zh`
2. Report matching listings: title, type, price (free/credits), installs, rating, one-line summary, and URL.
3. If nothing matches, suggest broader terms ("contract", "law") or dropping the filter.
