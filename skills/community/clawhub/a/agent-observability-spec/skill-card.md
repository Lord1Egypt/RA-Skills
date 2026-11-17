## Description:

Specifies tracing, metrics, alerting, sampling, retention, and privacy guidance for production AI agents and LLM features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define observability for an AI agent or LLM feature before or during production operation. It helps specify trace spans, metric families, alert owners, sampling, retention, dashboards, and privacy controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full-content tracing may capture user data, secrets, or sensitive prompts.

Mitigation: Require secret and PII redaction before ingestion, strict access controls, encryption, and documented deletion workflows.

Risk: Long retention of incident or full-content traces can expand privacy exposure.

Mitigation: Set explicit retention limits for full-content traces and restrict longer-lived incident traces to reviewed, access-gated records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/agent-observability-spec)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/agent-observability-spec.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown observability specification with tables and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the system shape, traffic volume, cost sensitivity, failure modes, and observability stack.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
