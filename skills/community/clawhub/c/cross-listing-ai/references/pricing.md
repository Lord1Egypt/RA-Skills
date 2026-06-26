# Pricing

Use this file when the seller wants a price suggestion.

## Pricing Strategy

- Use live comps first.
- Prefer sold comps over active listings.
- Match on brand, model, edition, condition, and completeness as closely as possible.
- Default to a `priced to sell` recommendation unless the seller asks to maximize margin.

## Research Order

1. Find recent sold comps for the same item or the closest credible equivalent.
2. Use active listings only when sold comps are sparse.
3. If comps are thin, fall back to heuristics from brand, category, rarity, and condition.
4. Adjust for missing accessories, defects, bundles, local-only delivery, and unusual demand.

## Output

Always return:

- suggested ask: the price you recommend posting
- expected sale range: a realistic range based on the comps
- confidence: high, medium, or low
- comp summary: 2-4 bullets explaining the best supporting comps
- links: include links when available through your tools

## Adjustment Rules

- Lower the suggested ask when the item is untested, incomplete, damaged, or poorly photographed.
- Raise the suggested ask when the item is complete, scarce, or unusually clean.
- For local-only marketplaces, consider the narrower buyer pool before suggesting an aggressive price.
- For TCG items, price the exact card and printing when possible. If the print or set is unclear, lower confidence and say why.

## Seller Communication

- Tell the seller what drove the number.
- Make uncertainty explicit when the comp set is weak.
- If the seller gives a target price, explain whether it is aligned with the comp range or likely optimistic.
