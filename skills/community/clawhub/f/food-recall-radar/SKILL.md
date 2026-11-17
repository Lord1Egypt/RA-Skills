---
name: food-recall-radar
description: "Use when you want to check whether food you actually bought is affected by an active recall, after hearing news of an outbreak or a brand recall, when organizing the pantry, after a grocery run, or on a schedule (weekly recall audit) — builds a personal pantry inventory of brands/products/UPCs, queries openFDA's live food-enforcement recall database, fuzzy-matches your items against ongoing Class I/II/III recalls with lot-code pattern extraction, and outputs a risk-ranked action list (check / discard / return-for-refund)."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [food-safety, recalls, pantry, openfda, health, household]
---

# Food Recall Radar

## Overview

Food recalls happen constantly — thousands per year in the US alone — but almost nobody hears about the one that affects *their* pantry. News covers outbreaks (Listeria in ice cream, Salmonella in eggs, undeclared peanuts in a cookie), not the 200 quieter recalls of store-brand products. The FDA's own estimate is that recalls reach consumers only a fraction of the time, and contaminated lots sit in kitchens for weeks. The gap isn't data — recalls are public within days — it's *matching*: nobody has the patience to cross-reference a scrolling recall list against their own groceries.

This skill closes that gap with a personal pantry inventory + live recall matching:

1. **Pantry inventory** — record what you buy (brand + product, optionally UPC and lot). A one-time 15-minute pantry scan, then 20 seconds per grocery run.
2. **Live matching** — pulls ongoing recalls from openFDA's food enforcement database (no API key required for light use) and fuzzy-matches against your items: brand containment, product-token overlap, sequence similarity.
3. **Lot intelligence** — extracts lot/code/date patterns from the recall notice and tells you exactly where to look on your package, instead of making you re-read the whole notice.
4. **Ranked actions** — Class I (reasonable probability of serious harm) first: *check the package / discard / return for refund*.

Everything is offline-first: pantry is local JSON, recall data can be cached with `--offline`, and the script is pure stdlib.

## When to Use

- **Heard about a recall/outbreak** — "wasn't there a spinach recall? did we buy that brand?" → `match`
- **Weekly household audit** — 30 seconds, catches the recalls you never heard of → `audit`
- **After a grocery run** — add new items in one command → `import-receipt`
- **Pantry reorganization / moving** — build the initial inventory → `add`
- **Vulnerable household** — pregnant, elderly, under-5, immunocompromised, allergies: undeclared allergen recalls are Class I for you even when rated II for the general public
- Don't use for: pet food (FDA maintains a separate animal-food enforcement file), drugs, or devices — different openFDA endpoints; and never for diagnosing illness — that's a doctor.

## Commands

```bash
# Record what you own (UPC optional but makes matching near-exact)
python3 scripts/recall_radar.py add --brand "Pillsbury" --product "Golden Layer Biscuits" \
    --upc 018000000000 --lot "K1234" --notes "bought 2026-08-30, fridge"
python3 scripts/recall_radar.py add --brand "Simple Truth" --product "Organic Baby Spinach 5oz"

# Paste a whole receipt / shopping list at once: "Brand Product" per line
python3 scripts/recall_radar.py import-receipt
Pillsbury Golden Layer Biscuits
Simple Truth Organic Baby Spinach 5oz
^D

# Check your pantry against LIVE ongoing recalls (openFDA)
python3 scripts/recall_radar.py match

# Broad weekly audit — active recalls + category heuristics even without brand hits
python3 scripts/recall_radar.py audit

# Use a cached JSON file instead of the network (offline / rate-limited)
python3 scripts/recall_radar.py match --offline --data references/sample-recalls.json

# Manage inventory
python3 scripts/recall_radar.py list
python3 scripts/recall_radar.py remove --brand "Simple Truth" --product "Organic Baby Spinach 5oz"
python3 scripts/recall_radar.py report          # full history of matched recalls
```

Pantry lives at `~/.pantry.json` (`--file` to override). An openFDA API key is optional (`--api-key` or `OPENFDA_API_KEY` env) — without one you get a lower rate limit, which a weekly household audit never approaches.

## How Matching Works (so you can trust or override it)

Every ongoing recall is scored against every pantry item on three signals:

| Signal | Meaning | Weight |
|---|---|---|
| Brand containment | your brand appears in the recall's recalling-firm or product description (fuzzy) | high |
| Product token overlap | shared meaningful words ("golden layer biscuits" vs "biscuits southern style") | medium |
| Sequence similarity | `SequenceMatcher` ratio on normalized strings | tie-breaker |

Scores above the threshold print with a `VERIFY` marker — a human looks at the package. UPC equality alone (when both sides have one) is a near-exact hit marked `MATCH`. The tool deliberately over-notifies: a false "go check the fridge" costs 10 seconds; a missed Class I *Listeria* exposure costs a lot more. Never discard food purely on the script's say-so — confirm against the linked recall notice, which is printed with every hit.

## Reading a Hit

```
[RISK 1] Class I  ── brand: Pillsbury / product: biscuits
  recall:     Soft biscuits recalled over Listeria monocytogenes
  firm:       Generic Foods Co.
  reason:     Listeria monocytogenes
  dates:      2026-08-01 → ongoing
  lot intel:  look for: lot codes starting 'K1', best-by 09/2026
  action:     DO NOT EAT — check package; return for refund or discard
  notice:     https://www.fda.gov/safety/recalls/...
```

Class I = reasonable probability of serious adverse health consequences (act now, especially for vulnerable household members). Class II = remote probability / temporary harm. Class III = unlikely to cause harm. Distribution dates tell you whether your purchase window overlaps.

## Common Pitfalls

1. **Trusting brand names literally.** Store brands are manufactured by third parties: "Simple Truth" spinach may be recalled under the co-packer's name. That's why `audit` also runs category heuristics (product-type words without a brand hit → `WATCH`).
2. **Ignoring UPC check digits.** If you type a UPC by hand and get a `MATCH` on a wrong-digit variant, verify the full 12-digit string against the package before discarding anything.
3. **Treating "no results" as "safe forever."** Recalls are matched against *ongoing* enforcement reports. Run `audit` weekly; newly announced recalls appear within days.
4. **Discarding without reading the notice.** Many recalls affect specific lots/plants/dates only. The printed notice URL states exactly which packages are affected — read it before throwing food away or demanding refunds.
5. **Rate limits.** Without an API key openFDA allows modest request volumes; a household runs 1–2 requests per week. If you script this hourly, get the free key and set `OPENFDA_API_KEY`.
6. **Allergen recalls and severity ratings.** A Class II "undeclared milk" is Class I *for your household* if someone is anaphylactic. Severity flags are population-level, not personal.

## Verification Checklist

- [ ] Pantry has at least the staples you'd be upset to hear were recalled (produce, dairy, frozen, pantry goods)
- [ ] `match` runs clean against live openFDA (or `--offline` with cached data)
- [ ] Every `VERIFY`/`MATCH` hit checked against the printed FDA notice URL
- [ ] `audit` scheduled weekly (add it to whatever runs your household chores)
- [ ] New grocery trips appended via `import-receipt` — 20 seconds, not a re-scan

## One-Shot Recipes

**"There was a recall on the news about ice cream"**
```bash
python3 scripts/recall_radar.py add --brand "Nice!" --product "Vanilla Ice Cream 48oz"
python3 scripts/recall_radar.py match
```

**Weekly Sunday audit (offline-first)**
```bash
python3 scripts/recall_radar.py audit --api-key "$OPENFDA_API_KEY"
```

**Testing the matcher without network**
```bash
python3 scripts/recall_radar.py add --brand "Tasty Blend" --product "Frozen Strawberries 12oz"
python3 scripts/recall_radar.py match --offline --data references/sample-recalls.json
```

**Vulnerable household member (pregnancy / chemo / toddler)**
```bash
python3 scripts/recall_radar.py audit   # weekly, minimum — Class I Listeria hits matter most
```
