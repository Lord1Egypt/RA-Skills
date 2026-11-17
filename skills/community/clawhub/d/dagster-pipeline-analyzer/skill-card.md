## Description:

Analyze Dagster pipelines and software-defined assets for quality, scheduling, partitioning, IO managers, resource configuration, and observability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Data platform developers and engineers use this skill to review Dagster projects for asset graph quality, freshness, partitioning, IO manager durability, resource configuration, schedules, sensors, and observability gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides an agent to inspect local Dagster project code and configuration, which may include sensitive deployment details.

Mitigation: Provide only the intended project path, keep access scoped to the review target, and review findings before applying any remediation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with shell commands, findings, recommendations, and remediation code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a health score, category breakdown, critical issue highlights, and remediation examples when supported by the analyzed Dagster project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
