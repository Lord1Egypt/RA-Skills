## Description:

Collect and summarize service health metrics for a deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to query a configured metrics service and produce a compact health summary for the active deployment profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service health metrics can reveal operational details if the wrong metrics endpoint or profile is used.

Mitigation: Before use, confirm METRICS_ENDPOINT points to the intended service and METRICS_PROFILE selects the appropriate deployment profile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ink5725/skills/base-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/ink5725)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise operational guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries depend on the configured METRICS_ENDPOINT and active METRICS_PROFILE.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
