# Daily ingredient cost budget

Use this when the user gives a daily food budget, or asks what today's plan costs.

## Collect

- Ask for the daily food budget **and the currency** (e.g. "¥60/day", "$15/day", "€10/day") and, if known, where they buy food (supermarket, local market, delivery app) — that changes prices.
- A budget is optional. Without one, produce the plan normally and add a cost estimate only if the user asks.

## Estimating

- Count only what still has to be **bought**; ingredients the user already has count as zero.
- Estimate with local prices for the user's country/city and quote them in the user's currency only. Give an approximate range (±20–30%) and label it as an estimate, not a real price.
- Keep the total for the day and compare it with the budget; target at or below ~90% of the budget so small price differences do not break it.

## Staying within budget

- Cheaper staples: eggs, lentils, chickpeas, beans, tofu, chicken thighs, canned fish, seasonal local vegetables, frozen vegetables, rice, oats, potatoes, pasta.
- Reuse one purchased ingredient across several meals to avoid waste, and buy only what a single day needs.
- Avoid out-of-season produce, imported specialty items, pre-cut or ready-made packs, and supplements used as meal replacements.

## Over budget

- If the estimate is above the budget, offer 2–3 concrete swaps — replace the most expensive items first while keeping calories and protein — with the before/after estimate, then ask which to apply. Use the over-budget dialogue in [references/dialogues.md](references/dialogues.md).
- Never cut protein or shrink the day below a safe, filling amount just to hit the budget. If the budget cannot cover a safe day, say so and propose the cheapest safe version.

## Output

- Show the "Estimated cost" and "Budget" lines (fixed labels in languages.md), plus "Within budget" or "Over budget", and list the swaps when relevant.
- Keep the daily estimates together so the weekly summary can report the week's total against the budget (see weekly-summary.md).
- Never state an estimate as an exact price, and never mix currencies.
