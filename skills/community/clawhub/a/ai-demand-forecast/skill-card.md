## Description:

Provides AI-supported demand and sales forecasting with replenishment planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External retail, supply chain, and inventory-planning teams use this skill to forecast demand or sales and draft replenishment plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path references mutable remote Python code that was not included in the reviewed artifact.

Mitigation: Review the external repository, pin a specific commit, and install only in an isolated environment before use.

Risk: Forecasting or replenishment recommendations may drive incorrect purchasing or inventory decisions.

Mitigation: Require human approval before acting on forecasts, replenishment plans, purchases, or inventory changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/ai-demand-forecast)
- [Publisher profile](https://clawhub.ai/user/yang1002378395-cmyk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise recommendations and inline shell commands when setup is discussed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecasting and replenishment outputs should be treated as recommendations requiring human approval before purchasing or inventory changes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
