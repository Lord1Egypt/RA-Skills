---
name: assortment-scout
description: Audit an ecommerce catalog, spot SKU sprawl, price and attribute coverage gaps, hero dependence, long-tail bloat, and duplicate-risk clusters, then turn rough catalog notes or CSV exports into keep-add-expand-merge-retire recommendations and a 30-day merchandising brief. Use when merchandisers, category managers, marketplace sellers, or consultants need assortment planning support without live ERP, PIM, or marketplace APIs.
---

# Assortment Scout

## Overview

Use this skill to turn catalog notes, export summaries, and merchandising goals into a practical assortment review. It is built for operators who need a fast decision layer for what to keep, expand, bundle, merge, or retire.

This MVP is heuristic. It does **not** access live Shopify, Amazon, ERP, PIM, or marketplace systems. It relies on the user's provided catalog structure, product performance notes, and business constraints.

## Trigger

Use this skill when the user wants to:
- reduce SKU clutter or long-tail bloat
- identify price-band, feature, or variant coverage gaps
- review duplicate-risk or cannibalization concerns
- prepare a category review, seasonal line review, or catalog cleanup memo
- turn pasted catalog notes into a prioritized merchandising action brief

### Example prompts
- "Audit our catalog for SKU clutter and hero-product dependence"
- "Find assortment gaps across our travel accessories line"
- "Which products should we keep, merge, bundle, or retire?"
- "Create an assortment review from these catalog and margin notes"

## Workflow

1. Capture the review objective, such as cleanup, gap discovery, expansion planning, or seasonal review.
2. Normalize the likely assortment signals: revenue, margin, returns, inventory, and variant coverage.
3. Apply a portfolio lens across hero, core, seasonal, long-tail, and duplicate-risk products.
4. Highlight likely gap areas, overlap clusters, and execution priorities.
5. Return a markdown brief with keep-add-expand-merge-retire guidance and a 30-day plan.

## Inputs

The user can provide any mix of:
- catalog exports or summarized SKU lists
- category, subcategory, price, margin, and launch-age notes
- performance signals such as revenue, units, conversion, returns, ratings, or sell-through
- variant structure such as size, color, pack size, or material
- business goals such as premiumization, bundle strategy, entry-price coverage, or seasonal cleanup
- operating constraints such as shelf space, warehouse capacity, cash limits, or protected hero products

## Outputs

Return a markdown assortment brief with:
- assortment health summary
- scorecard lenses and evidence gaps
- coverage and gap map
- duplicate-risk or cannibalization watchlist
- keep-add-expand-merge-retire recommendations
- 30-day execution brief with likely owners
- assumptions, confidence notes, and limits

## Safety

- Do not claim access to live catalog or marketplace data.
- Treat cannibalization as an informed hypothesis, not proven causality.
- Do not auto-retire, merge, or reprice products.
- Downgrade recommendations when taxonomy, margin, or demand evidence is incomplete.
- Keep strategic SKU decisions human-approved.

## Best-fit Scenarios

- DTC or marketplace catalogs with roughly 30 to 2,000 active SKUs
- regular category reviews, quarterly assortment planning, or pre-promo cleanup
- teams that want a lighter decision layer than a full merchandise-planning suite
- consultants who need a fast first-pass assortment memo

## Not Ideal For

- store-level planogram planning for large physical retail networks
- businesses with no structured catalog or product taxonomy at all
- workflows that need automatic listing edits, delisting, or system sync
- highly regulated approvals where assortment change requires formal governance

## Example Output Pattern

A strong response should:
- show the likely assortment shape, not just list products
- separate hero, core, seasonal, long-tail, and duplicate-risk logic
- explain where the catalog is overbuilt or under-covered
- recommend next actions with impact, confidence, and owner hints
- include a short assumptions block when the evidence is partial

## Acceptance Criteria

- Return markdown text.
- Include health, gap, recommendation, and execution sections.
- Make the advisory framing explicit.
- Keep the brief practical for merchandisers and ecommerce operators.
