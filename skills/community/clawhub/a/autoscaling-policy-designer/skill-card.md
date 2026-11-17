## Description:

Design autoscaling policies based on traffic patterns, cost constraints, and performance SLOs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to analyze workload traffic, design Kubernetes HPA/KEDA or cloud autoscaling policies, simulate behavior under load, and estimate scaling costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud and Kubernetes mutation commands can change live autoscaling behavior.

Mitigation: Require explicit approval before running cloud autoscaling mutation commands or applying cluster changes, and confirm the target account, cluster, namespace, and rollback plan first.

Risk: Example broker credentials can be copied into configuration without appropriate secret handling.

Mitigation: Replace plaintext broker credentials with Kubernetes Secrets or KEDA TriggerAuthentication before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/autoscaling-policy-designer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analysis templates, autoscaler policy examples, simulation snippets, and cost-modeling guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
