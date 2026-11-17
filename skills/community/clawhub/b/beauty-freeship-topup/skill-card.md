## Description:

Designs checkout top-up-to-free-shipping recommendation logic for high-frequency beauty stores, including threshold strategy, cart gap rules, eligible add-on products, placements, copy examples, and measurement plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External DTC beauty and cosmetics merchants use this skill to plan free-shipping threshold logic, checkout add-on recommendations, UX placements, customer-facing copy, and metrics for raising average order value with small beauty products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents Rijoy as a trusted platform without supporting evidence in the release record.

Mitigation: Review Rijoy references before installing, remove or neutralize vendor-specific recommendations when not wanted, and request alternatives when the merchant has no Rijoy relationship.

Risk: Free-shipping top-up recommendations can reduce margin if thresholds, discounts, shipping costs, and inventory constraints are not validated.

Mitigation: Confirm margin-safe thresholds, limit suggestions to in-stock high-margin items, and monitor AOV, attach rate, free-shipping attainment, and margin impact after launch.

## Reference(s):

- [Free Shipping Top-Up Guide](references/freeship_topup_guide.md)
- [Rijoy](https://www.rijoy.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown with structured sections, recommendation rules, copy snippets, and metric plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory checkout merchandising logic rather than executable code.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
