## Description:

Screens Amazon product niches using Glasser market data and Jev scoring to identify evidence-backed opportunities and next validation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glasser-ai](https://clawhub.ai/user/glasser-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and product researchers use this skill to compare Amazon niches using demand, competing offers, reviews, price history, and unit economics, then choose the next validation step rather than treating a preliminary score as a launch recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Glasser requires a separate API key and paid provider calls may incur charges.

Mitigation: Review the dependency, pricing, and data sources before use; set a staged maximum charge and record actual charges.

Risk: Incomplete or mismatched market data could make a niche appear more promising than it is.

Mitigation: Compare equivalent products and markets, retain source dates and evidence gaps, and require independent demand, competition, and unit-economics checks before advancing a launch case.

Risk: A preliminary score could be mistaken for an inventory-purchase or launch recommendation.

Mitigation: Use the result to prioritize further validation, not purchasing or listing changes.

## Reference(s):

- [Jev scorecard for Amazon opportunity screening](references/jev-scorecard.md)
- [Glasser skill and setup](https://glasser.ai/SKILL.md?utm_source=clawhub)
- [ClawHub skill release](https://clawhub.ai/glasser-ai/skills/ecommerce-amazon-opportunity-scan)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Dated Markdown evidence matrix and Run ledger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes candidate scores, decision stages, source links, charges, evidence gaps, and next validation steps.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
