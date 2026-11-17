## Description:

Record every tool call into agent-tracer (self-hosted FastAPI), then run regression testing (golden case → drift detection), attribute token costs by tool/model/agent, and surface recurring error root causes across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wholegale39](https://clawhub.ai/user/wholegale39)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to instrument agent runs, compare new runs against golden cases, attribute model and tool costs, and identify recurring error patterns across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent activity may be stored in the tracer, including sensitive tool arguments, results, private files, customer data, or personal data.

Mitigation: Redact secrets and sensitive data before logging, and define a retention and deletion plan before production use.

Risk: The tracing service is described as a network service and could expose agent traces if deployed beyond local development without controls.

Mitigation: Keep the service bound to localhost unless authentication, TLS, and firewall controls are in place.

Risk: Security evidence rates the release as suspicious because broad raw logging is encouraged without enough privacy, security, or deployment safeguards.

Mitigation: Review the deployment model and logging policy before installation, using the security guidance as the authoritative risk baseline.

## Reference(s):

- [agent-tracer ClawHub page](https://clawhub.ai/wholegale39/skills/agent-tracer)
- [agent-tracer source repository](https://github.com/wholegale39/agent-tracer)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and API endpoint tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on trace recording, regression checks, cost attribution, and error aggregation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
