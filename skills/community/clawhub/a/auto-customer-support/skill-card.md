## Description:

Provides a lightweight FAQ-based customer support scaffold with automated replies, webhook intake, and handoff or ticket escalation paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xianji520](https://clawhub.ai/user/xianji520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support operations teams use this skill to scaffold FAQ-driven customer support automation, test sample conversations, and prepare webhook or ticket-system integrations with human escalation when confidence is low.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runnable server is configured with debug mode and binds to all interfaces.

Mitigation: Disable debug mode and bind to localhost or a protected interface before any shared or production deployment.

Risk: Webhook and escalation routes are unauthenticated.

Mitigation: Add authentication or signature validation, request validation, and rate limits before connecting external channels.

Risk: Unpinned dependencies can change behavior or introduce vulnerable versions.

Mitigation: Pin and review dependencies before deployment.

Risk: Automated support replies may be sent to real customer channels before controls are ready.

Mitigation: Test in a controlled environment and do not connect real customer channels or ticket systems until security controls and reply quality are reviewed.

## Reference(s):

- [Channel Integration Guide](references/integration-guides.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code, shell commands, configuration notes, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces FAQ reply text and escalation indicators; runtime webhook responses are JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
