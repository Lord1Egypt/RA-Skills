## Description:

Design chaos engineering experiments to test system resilience. Generate failure injection scenarios, define steady-state hypotheses, blast radius controls, and rollback procedures for services, networks, and infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use this skill to design chaos experiments, game days, readiness audits, and result reports for services, networks, and infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production-targeted failure examples can cause service disruption if copied directly into live environments.

Mitigation: Treat generated commands as design drafts; require explicit non-production defaults, dry runs, rollback readiness, health checks, and human approval before failure injection.

Risk: Broad Kubernetes discovery can inspect more namespaces than intended.

Mitigation: Limit Kubernetes context and namespace scope before use, and only inspect cluster resources that are authorized for the exercise.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/chaos-test-designer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include chaos experiment definitions, game day plans, readiness scores, rollback procedures, and remediation recommendations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
