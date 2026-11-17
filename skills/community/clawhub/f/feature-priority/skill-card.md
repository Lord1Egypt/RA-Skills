## Description:

Ranks Amazon product improvement features by review frequency and customer impact, using product details as context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and product operators use the skill to prioritize product feature improvements from recurring review themes and customer impact, with review evidence supporting recommendations.

### Deployment Geography for Use:

Amazon marketplaces in the United States, United Kingdom, Germany, Japan, Canada, France, Spain, and Italy.

## Known Risks and Mitigations:

Risk: The skill exposes paid ARI services beyond feature ranking and may spend account credits without clear approval.

Mitigation: Review before installing, require approval for each quoted cost, disable account auto-confirmation, and separately approve recurring collection. Request a corrected package that enforces the advertised scope and quote-only fallback.

## Reference(s):

- [ARI CLI and API reference](artifact/references/reference.md)
- [Product operations workflow](artifact/references/operation-workflow.md)
- [ARI Product Operations](https://ari.funewa.com/zh/operations)
- [ARI Monitor Center](https://ari.funewa.com/zh/monitor)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Concise text or Markdown product analysis and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations should state their review evidence and data scope; paid actions and recurring collection require clear authorization.]

## Skill Version(s):

1.5.3 (source: server release evidence, _meta.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
