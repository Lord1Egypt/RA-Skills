## Description:

Cross Agent Chat standardizes how agents discover target sessions and send messages to other agents through sessions_send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ebly](https://clawhub.ai/user/ebly)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to coordinate work with other agents by finding a target session, sending a clear request, and waiting for a response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages sent to another session may expose secrets, credentials, personal data, internal prompts, or unrelated user content.

Mitigation: Confirm the target session is authorized and remove sensitive or unrelated content before sending a message.

Risk: A request may be sent to the wrong agent if the target session is guessed or stale.

Mitigation: Use sessions_list to confirm the target session identifier before sending cross-agent messages.

## Reference(s):

- [Cross Agent Chat on ClawHub](https://clawhub.ai/ebly/skills/cross-agent-chat)
- [Publisher profile: ebly](https://clawhub.ai/user/ebly)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces messaging workflow guidance and example sessions_send requests; it does not include executable code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
