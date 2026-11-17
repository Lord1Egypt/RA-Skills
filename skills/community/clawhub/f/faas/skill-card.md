## Description:

Faas guides developers through designing and debugging serverless workloads across event sources, IAM, cold starts, limits, observability, security, cost, and deployment patterns for functions, containers, step functions, and edge workers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess whether serverless is a good fit, design event and retry contracts, review IAM and networking, tune runtime performance, improve observability, and control cost for cloud function and edge worker workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud IAM policies or deployment changes produced during use could affect cost, availability, or access control.

Mitigation: Review generated IAM policies, network settings, and deployment changes before applying them.

Risk: Serverless workloads can incur unexpected cost from recursive invocations, retries, or over-provisioned concurrency.

Mitigation: Use budgets, billing alerts, anomaly detection, and explicit retry and dead-letter policies.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Code, Shell commands]

**Output Format:** [Markdown guidance with checklists and optional code, configuration, or shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only skill; any proposed cloud IAM policies, deployment changes, or runtime settings should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
