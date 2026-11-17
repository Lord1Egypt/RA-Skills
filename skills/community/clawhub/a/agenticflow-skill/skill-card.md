## Description:

Créer la proposition du Skill AgenticFlow pour automatiser LinkedIn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgreselin-create](https://clawhub.ai/user/cgreselin-create)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan LinkedIn automation workflows for publishing content, managing private messages and invitations, and retrieving engagement statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad LinkedIn account automation may post content, read private messages, send replies, manage contacts, and collect analytics without clear separate approvals.

Mitigation: Require separate opt-in controls for posting, private-message reading, message sending, contact management, analytics, and daily summaries.

Risk: Automated message replies or contact actions could reach unintended recipients or use unintended final text.

Mitigation: Confirm recipients and final message text before anything is sent or accepted.

Risk: Use may exceed platform limits or fail during OAuth token handling.

Mitigation: Respect LinkedIn API rate limits and review OAuth refresh handling before deployment.

## Reference(s):

- [Agenticflow Skill on ClawHub](https://clawhub.ai/cgreselin-create/skills/agenticflow-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with workflow steps and configuration requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LinkedIn account, API or OAuth access, and user confirmation before account actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
