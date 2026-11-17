## Description:

Detect and resolve backpressure issues in data pipelines, message queues, and streaming systems. Identify bottleneck stages, measure queue depths and processing rates, and recommend flow control strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to diagnose pipeline slowdowns, growing queues, and consumer lag across message queues and streaming systems. It helps identify bottleneck stages and draft flow-control, autoscaling, alerting, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic commands may reveal operational topology, queue names, consumer groups, or metrics labels.

Mitigation: Review commands before execution, use read-only credentials, and avoid sharing raw command output outside authorized teams.

Risk: Generated remediation guidance such as autoscaling, rate limiting, or load shedding can affect production behavior if applied directly.

Mitigation: Treat recommendations as operator-reviewed proposals and test changes in a controlled environment before production rollout.

Risk: Metrics endpoint and queue queries can expose sensitive operational data even when they do not modify systems.

Mitigation: Run diagnostics only against authorized systems and redact queue names, service names, and topology details from reports when needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic command snippets, backpressure analysis reports, flow-control recommendations, and Prometheus alert rule examples.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
