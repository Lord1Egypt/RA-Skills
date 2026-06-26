# Workflow

Use this file for the end-to-end seller flow.

## Hidden Reviewed-Item Record

Track these fields internally:

- item identity: brand, model, product name, variant, bundle contents
- condition: overall grade plus evidence that supports it
- category: broad marketplace-facing category
- attributes: material facts that can be reused across marketplaces
- missing facts: details you still need from the seller
- uncertainties: facts suggested by the images but not confirmed
- optional TCG details: card name, game, set, card number, finish, language, rarity
- pricing rationale: comp notes, adjustments, confidence
- seller-confirmed price: the price they want to post at
- selected marketplaces: eBay, Mercari, Facebook Marketplace, Craigslist, TCGPlayer

Keep this record internal. Present summaries in plain language only when helpful.

## Phase Gates

### Intake

- Confirm what the seller wants to sell.
- Confirm which marketplaces they want to target.
- Ask whether they want a fast sale or a higher asking price.
- Ask for any known facts the photos may not reveal, such as defects, accessories, or local-only constraints.

### Extract

- Inspect the item photos and draft the reviewed-item record.
- Separate confirmed facts from likely but unconfirmed facts.
- If a detail matters for condition, fit, authenticity, or value, carry it into `missing facts` or `uncertainties`.

### Clarify

- Ask the fewest questions that unlock the biggest pricing or marketplace decisions.
- Prefer questions about identity, condition, completeness, defects, and local pickup or shipping constraints.
- If the seller does not know a detail, keep the uncertainty explicit instead of guessing.

### Price

- Research comps only after the item identity and condition are good enough to compare responsibly.
- Produce a suggested ask, expected sale range, confidence level, and a short explanation of the comps.

### Confirm

- Summarize the item and recommended price naturally.
- Ask the seller to correct anything wrong before marketplace copy is generated.

### Generate

- Load `references/final-output.md` and the selected marketplace briefs.
- Generate only the marketplaces the seller requested.
- If one marketplace is blocked, continue with the others and explain the skip clearly.

### Revise

- When the seller changes facts, update the reviewed-item record first.
- Regenerate only the affected marketplace outputs and price recommendation.

## Mandatory Gating

- Never invent shipping, authenticity, or condition claims.
- Treat unresolved identity or condition questions as blockers for pricing and final copy.
- Treat unresolved `card name`, `game`, or `set` as blockers for TCGPlayer only.
