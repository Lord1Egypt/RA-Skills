## Description:

Send Discord Components v2 interactive messages (buttons, selects, modals, rich layouts) via the message tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muselinn](https://clawhub.ai/user/muselinn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to compose OpenClaw message tool payloads for Discord confirmations, selections, status cards, modal forms, and rich component layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary typed messages could be mistaken for trusted button clicks or selections in restricted or destructive workflows.

Mitigation: Use this skill for consequential actions only where trusted interaction metadata is available, or where the agent independently verifies the user, channel, original message, action ID, workflow state, and expiry before acting.

Risk: Reusable or delayed interactions can arrive after the original workflow context is no longer valid.

Mitigation: Check the current workflow state and expiry before executing an action, and update the Discord message when an interaction is expired or invalid.

Risk: Buttons for approvals, deployments, deletion, moderation, or similar actions may be clicked by unintended users if access is not restricted.

Mitigation: Use allowedUsers for restricted actions and verify the actor before carrying out sensitive operations.

## Reference(s):

- [Discord Interactive ClawHub Skill Page](https://clawhub.ai/muselinn/skills/discord-interactive)
- [Components v2 Reference](references/components.md)
- [Component Examples](references/examples.md)
- [Handling Component Interactions](references/handling.md)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with JSON5 message payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Discord component payload patterns for the OpenClaw message tool; no executable files are generated.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
