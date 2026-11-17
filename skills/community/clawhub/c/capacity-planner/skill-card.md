## Description:

Forecast infrastructure capacity needs using historical metrics, growth projections, and cost modeling. Identify bottlenecks before they cause outages and right-size resources to avoid over-provisioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, infrastructure engineers, and operators use this skill to forecast resource exhaustion, identify capacity bottlenecks, recommend right-sized infrastructure, and model future infrastructure costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Capacity queries can expose operational metadata such as instance names, utilization, disk capacity, database connection limits, and cloud account context.

Mitigation: Review the Prometheus URL, cloud account, command scope, and returned metrics before sharing outputs or acting on recommendations.

Risk: Forecasts and right-sizing recommendations can be misleading if they rely on incomplete historical metrics, short windows, or unsuitable growth assumptions.

Mitigation: Validate forecast inputs, growth model assumptions, and proposed infrastructure changes against current monitoring data and operational requirements before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and capacity-planning report tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include infrastructure queries, growth calculations, forecast summaries, bottleneck rankings, and cost recommendations.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
