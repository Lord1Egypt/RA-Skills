## Description:

Provides a free Cerebratech CogDx cognitive health check that sends 10-20 recent agent outputs to an API and returns one concrete calibration or reasoning finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drkavner](https://clawhub.ai/user/drkavner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to submit recent outputs with confidence and correctness labels for a lightweight cognitive health check before deciding whether to run deeper paid diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent prompts and responses may contain sensitive, proprietary, personal, customer, or regulated data that would be sent to a third-party API.

Mitigation: Use only redacted, non-confidential examples unless the publisher provides acceptable consent, retention, deletion, and privacy guarantees.

## Reference(s):

- [CogDx Health Check API Reference](references/api.md)
- [CogDx Repository](https://github.com/drkavner/cogdx)
- [CogDx Health Check on ClawHub](https://clawhub.ai/drkavner/skills/cogdx-health)
- [Cerebratech CogDx Health API](https://api.cerebratech.ai/cogdx-health)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one diagnostic finding with supporting evidence, severity, recommendation, and next-step guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
