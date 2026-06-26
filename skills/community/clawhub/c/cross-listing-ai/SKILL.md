---
name: cross-listing-ai
description: Guide an OpenClaw agent through seller-side cross listing and marketplace-ready listing generation from item photos. Use when the seller wants a listing AI workflow for image analysis, freeform clarification, live-comp pricing, or copy-paste-ready listing descriptions for eBay, Mercari, Facebook Marketplace, Craigslist, or TCGPlayer.
---

# OpenClaw Seller Cross Listing AI

Keep the seller experience conversational while you maintain a hidden reviewed-item record.

## Non-Negotiables

- Do not invent facts that are not visible in the images or confirmed by the seller.
- Keep the reviewed-item record internal. Surface concise natural-language summaries, not JSON.
- Use this phase flow exactly: `intake -> extract -> clarify -> price -> confirm -> generate -> revise`.
- Do not enter `price` until you have enough identity and condition detail to research comps responsibly.
- Do not enter `generate` until the blocking missing facts are resolved or the seller explicitly chooses to skip a marketplace.
- Default pricing posture is `priced to sell` unless the seller asks for a different goal.
- Only generate `TCGPlayer` output when `card name`, `game`, and `set` are known.

## Reference Routing

- Open `references/workflow.md` first for the end-to-end seller flow and the hidden reviewed-item record.
- Open `references/extraction.md` when you are turning images into item facts, condition notes, missing facts, or uncertainties.
- Open `references/pricing.md` when you are ready to research live comps and suggest a price.
- Open `references/final-output.md` immediately before drafting the final seller-facing response.
- Open only the marketplace briefs the seller selected:
  - `references/marketplaces/ebay.md`
  - `references/marketplaces/mercari.md`
  - `references/marketplaces/facebook-marketplace.md`
  - `references/marketplaces/craigslist.md`
  - `references/marketplaces/tcgplayer.md`
- Open `references/examples.md` only when you need a compact model for tone, sequencing, or edge-case handling.

## Working Rules

- Start at `intake`: confirm what the item is, what photos are available, which marketplaces the seller wants, and whether they care more about speed or margin.
- Move to `extract`: inspect the images and build a provisional internal record with facts, missing fields, and uncertainties.
- Move to `clarify`: ask only the highest-value follow-up questions needed to resolve identity, condition, completeness, and marketplace gating.
- Move to `price`: use live comps first, then heuristics only when the market data is thin.
- Move to `confirm`: summarize the reviewed item and price recommendation in prose, then invite corrections.
- Move to `generate`: produce copy-paste-ready output for each selected marketplace using `references/final-output.md` plus the relevant marketplace briefs.
- Move to `revise`: if the seller changes facts, price, or marketplaces, update the internal record first and regenerate only the affected output.
