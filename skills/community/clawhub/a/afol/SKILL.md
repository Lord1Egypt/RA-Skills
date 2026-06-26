---
name: afol
description: Use this orchestration skill to choose the right AFOL provider skill for catalog lookup, marketplace pricing, collection management, valuation, and cross-provider workflows.
version: 1.0.0
---

# AFOL meta skill

Use this skill when the user asks a broad AFOL collector question and it is not obvious which provider-specific skill should handle it. This is the human-facing router over the provider skills, not another vendor API wrapper.

Primary interface: `scripts/afol`.

The skill composes the checked-in provider skills and keeps orchestration guidance inside this skill directory:
- Orchestration reference: `references/prompts/afol-router.txt`
- CLI source: `scripts/afol_cli.py`
- Metadata-only OpenAPI placeholder: `references/openapi/afol.yaml`

Do not route through the Brick Directory app by default. Prefer the official provider skills directly. Brick Directory may be useful later for app-specific rendered reports or internal cross-provider mappings, but it is not the canonical data layer for this skill.

## Provider routing

| User intent | Start with | Then use | Why |
|---|---|---|---|
| Find a set, part, minifig, element, color, theme, or inventory | `rebrickable` | `brickset` for richer set metadata | Rebrickable is the canonical catalog/data backbone. |
| Exact set metadata, images, instructions, reviews, release status, owned/wanted context | `brickset` | `rebrickable` for inventory/parts | Brickset has strong editorial/set metadata and user collection fields. |
| Marketplace pricing, price guides, orders, inventory, feedback, coupons, member notes | `bricklink` | `brickowl` for marketplace comparison | BrickLink is the main marketplace and price-guide source. |
| BrickOwl store inventory, catalog ID lookup, listing management | `brickowl` | `bricklink` for market comparison | BrickOwl has separate store/catalog IDs and marketplace workflows. |
| Set or minifig valuation, forecasts, growth, ROI, collection performance, sales ledger | `brickeconomy` | `bricklink` for current market validation | BrickEconomy is the value/forecasting provider. |
| Cross-provider ID translation | `rebrickable` | `bricklink`, `brickowl`, `brickset` | Normalize to stable catalog IDs first, then fan out. |
| “Tell me everything about set X” | `rebrickable` + `brickset` | `brickeconomy`, then marketplaces if pricing is requested | Avoid expensive/bulk pricing unless the user asked for it. |

## Credential readiness

Use `scripts/afol credentials` to check which capabilities are unlocked without printing secret values.

Provider env vars:

```bash
export REBRICKABLE_API_KEY=...          # catalog lookup and public Rebrickable reads
export REBRICKABLE_USER_TOKEN=...       # optional private Rebrickable collection reads/writes
export BRICKSET_API_KEY=...             # Brickset public reads
export BRICKSET_USER_HASH=...           # optional private Brickset collection/wishlist/notes
export BRICKOWL_API_KEY=...             # BrickOwl store/account reads and guarded writes
export BRICKLINK_API_CONSUMER_KEY=...   # BrickLink OAuth1 credential set
export BRICKLINK_API_CONSUMER_SECRET=...
export BRICKLINK_API_TOKEN_VALUE=...
export BRICKLINK_API_TOKEN_SECRET=...
export BRICKECONOMY_API_KEY=...         # BrickEconomy valuation and private portfolio reads
```

Never print, commit, log, or paste real credentials. Report only whether each provider is ready.

## CLI quick reference

Run commands from this skill directory:

```bash
scripts/afol --help
scripts/afol route "What is set 10236-1 worth?"
scripts/afol route "Find parts for Millennium Falcon"
scripts/afol route "Compare BrickLink and BrickOwl price for 3001 red"
scripts/afol credentials
```

The CLI does not call provider APIs. It gives deterministic routing and credential-readiness hints so an agent can load/use the correct provider skill next.

## Canonical workflows

### “Tell me everything about set 10236-1”

1. Use `rebrickable set --set-num 10236-1` for canonical set identity and basic catalog data.
2. Use `rebrickable set-parts --set-num 10236-1` only if inventory/parts matter.
3. Use `brickset details --set-number 10236-1` for richer metadata, images, instructions, release status, ratings, and Brickset IDs.
4. Use `brickeconomy set --set-number 10236-1 --currency <currency>` only when the user asks about value, ROI, investment, or current/forecast prices.
5. Use marketplace provider skills only when the user asks about buying, selling, price guides, or listings.

### “What is this minifig worth?”

1. Identify the minifig number with `rebrickable minifigs --search ...` if the user did not provide one.
2. Use `brickeconomy minifig --minifig-number <id> --currency <currency>` for valuation and forecast fields.
3. Use `bricklink` price-guide or item lookup only if the user asks for market validation or current marketplace pricing.

### “Compare BrickLink vs BrickOwl price”

1. Resolve the entity first; do not guess provider IDs.
2. Use BrickLink and BrickOwl read-only lookup/price/catalog commands.
3. Report assumptions clearly: item type, color, condition, currency, quantity, and whether shipping is included.
4. Do not create listings, orders, feedback, member notes, or coupons unless the user explicitly asks and approves the exact write.

### “Prepare collection valuation”

1. Prefer one collection endpoint over many individual lookups.
2. Use `brickeconomy collection-sets` / `collection-minifigs` for value, growth, and ROI when available.
3. Use Rebrickable or Brickset private collection endpoints only if the matching user token/hash is configured and the user asked for private collection analysis.
4. Treat collection and sales-ledger payloads as private financial/account data; summarize, do not dump raw rows.

### “Find IDs across providers”

1. Start from Rebrickable set/part/minifig/color identity when possible.
2. Use provider-specific mapping or lookup commands for BrickLink, BrickOwl, and Brickset.
3. If an official reference lacks an endpoint for a mapping, say so; do not invent IDs.
4. Keep null/not-found distinct from not-checked-yet.

## Safety rules

Read-only by default. Credentials are capability, not consent.

Writes are allowed only after explicit current-conversation user intent and the provider skill’s mechanical guard:
- Rebrickable list/set/part writes require the Rebrickable skill’s `--yes`; use `--dry-run` first.
- Brickset collection/wishlist writes require the Brickset skill’s `--yes`; use `--dry-run` first.
- BrickOwl inventory writes/deletes require the BrickOwl skill’s `--yes`; use `--dry-run` first.
- BrickLink inventory/order/feedback/coupon/member-note writes require the BrickLink skill’s `--yes`; use `--dry-run` first.
- BrickEconomy is currently read-only in this skill pack, but private collection and sales-ledger reads are still sensitive.

Never checkout, order, buy, sell, update inventory, delete listings, post feedback, or alter collections from inference alone.

## Common pitfalls

1. **Starting with marketplace APIs for identity questions.** Use Rebrickable or Brickset first; marketplaces are noisy and condition/currency-sensitive.
2. **Treating Brick Directory as the source of truth.** The app is optional glue. The durable layer is provider skills over official APIs.
3. **Bulk fan-out by habit.** BrickEconomy has tight limits; marketplace calls can be expensive/noisy. Start narrow.
4. **Leaking private data.** Collection, inventory, order, store, and sales-ledger data should be summarized, not pasted raw.
5. **Guessing IDs.** Resolve IDs via provider lookup/mapping commands instead of fabricating BrickLink, BrickOwl, Brickset, or Rebrickable IDs.
6. **Letting credentials imply approval.** They only prove access; writes still need explicit approval and provider guard flags.

## Live smoke checks

Local, no-network checks:

```bash
python3 -m py_compile scripts/afol_cli.py
scripts/afol route "What is set 10236-1 worth?"
scripts/afol credentials
```

Provider live smoke tests belong in the provider skills. This meta skill should not call external APIs itself.

## Verification checklist

- [ ] Route catalog/identity questions to Rebrickable or Brickset first.
- [ ] Route valuation/forecasting to BrickEconomy.
- [ ] Route marketplace, inventory, order, feedback, coupon, and member-note workflows to BrickLink or BrickOwl.
- [ ] Keep Brick Directory optional, never a dependency for provider data.
- [ ] Report credential readiness without printing secret values.
- [ ] Use provider skill dry-runs and `--yes` guards for any write.
