## Description:

Track SLO error budgets across services. Calculate remaining budget from SLI metrics, alert on budget burn rate, recommend development vs reliability investment, and generate error budget reports for stakeholder review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reliability engineers use this skill to calculate service error budget status, review SLO burn rates, draft alerts, and prepare stakeholder-facing reliability guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples for querying monitoring systems such as Prometheus.

Mitigation: Install and use it only where the agent is allowed to query the organization's monitoring system.

Risk: Generated deploy-freeze, reliability investment, and policy recommendations may be incorrect or incomplete for a service's operational context.

Mitigation: Review recommendations with service owners or reliability engineers before acting on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML, bash, Python, and policy examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates analysis and recommendations for review; it does not enforce deploy freezes or reliability controls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
