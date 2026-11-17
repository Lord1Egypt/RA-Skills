## Description:

Generates ecommerce pricing strategy recommendations, including pricing model selection, profit optimization, promotion formulas, and platform-specific pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ecommerce operators, and pricing analysts use this skill to calculate suggested prices, promotion plans, and bundle strategies from cost, competitor prices, target platform, and action type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pricing inputs such as product cost and platform selection may be written to local logs by the helper script.

Mitigation: Avoid confidential cost data on shared systems and restrict local log access when using the helper.

Risk: Pricing recommendations may be incorrect or unsuitable for a specific store, promotion, or marketplace policy.

Mitigation: Review outputs before applying prices in commerce platforms and use separate controlled tooling for any price changes.

## Reference(s):

- [Business Rules](references/business_rules.md)
- [Error Codes](references/error_codes.md)
- [Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/ecommerce-pricing-strategy)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON from the helper script, with concise text or Markdown recommendations when used conversationally]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local pricing-planning recommendations; it does not execute price changes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
