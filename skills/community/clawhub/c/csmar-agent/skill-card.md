## Description:

Provides access to CSMAR financial-report APIs for A-share company financial-report queries and streams the returned content without adding a final summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmpx8](https://clawhub.ai/user/xmpx8)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to answer A-share company financial-report questions through the CSMAR backend, especially when prompts mention finance-related keywords or @csmar_agent / @csmar-agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User financial queries are sent to an opaque hardcoded private backend over plaintext HTTP.

Mitigation: Install only after confirming the backend operator, service behavior, transport protections, retention policy, and access controls.

Risk: Queries may include confidential research, customer data, credentials, or internal business context.

Mitigation: Avoid sending sensitive information unless the publisher documents appropriate service, transport, retention, and access controls.

## Reference(s):

- [csmar-agent on ClawHub](https://clawhub.ai/xmpx8/skills/csmar-agent)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text streamed to the terminal or agent response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streams non-empty content chunks as they arrive and does not add wrapping text or a final summary.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
