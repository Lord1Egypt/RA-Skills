## Description:

Use when evaluating any sale, Black Friday doorbuster, or 'was $X now $Y' claim: detects fake-MSRP anchoring, pre-sale price inflation, coupon-stacking theater, and % off a price nobody paid. Scores the deal against 12-month category price bands and historical-low baselines, with verdicts WAIT / OK DEAL / GREAT / PRICE THEATER.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Shoppers and agents use this skill to assess sale claims against current street prices and 12-month lows, identify common price-theater tactics, and decide whether to buy or wait.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deal scores are estimates and depend on verified price inputs, price timelines, coupon conditions, and fixed calculator assumptions for gift cards and membership fees.

Mitigation: Verify current street prices and historical lows, check price timelines and coupon conditions separately, and account for actual gift-card value and membership cost; the calculator values gift cards at 50% and allocates 30% of a membership fee to the purchase.

## Reference(s):

- [price-theater.md](references/price-theater.md)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/black-friday-deal-detector)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, JSON]

**Output Format:** [Deal verdict and buying strategy in text, with optional JSON from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assesses a single offer or compares two offers using supplied price inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
