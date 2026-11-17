## Description:

Analyzes competitor ecommerce price history through Glasser for exact Amazon product variants, highlighting unusual changes, their duration, and relevant pricing context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glasser-ai](https://clawhub.ai/user/glasser-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Retail analysts and ecommerce teams use this skill to examine historical Amazon price changes for an exact competitor product, compare them with a baseline, and plan monitoring thresholds. Optional current merchant comparisons are identified separately from historical prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runs can incur charges from paid data providers, including runs that return no usable history.

Mitigation: Review the Glasser dependency and expected cost, use a budget cap, start with one product, and report each run's actual charge and outcome.

Risk: Variant mismatches, missing price intervals, or differing price types can mislead pricing decisions.

Mitigation: Verify the exact product and price series, disclose unavailable periods and thresholds, and label current shopping quotes separately from historical prices.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/glasser-ai/skills/ecommerce-competitor-price-monitor)
- [Glasser skill and installation guide](https://glasser.ai/SKILL.md?utm_source=clawhub)
- [Keepa product history specification](https://keepa.com/api-docs/product-object.html)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown price-history table and narrative; optional machine-readable analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes product identity, observation dates, price basis, unavailable periods, thresholds, and actual provider charges.]

## Skill Version(s):

0.1.0 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
