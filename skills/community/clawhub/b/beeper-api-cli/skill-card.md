## Description:

Read and send messages via Beeper CLI. Supports WhatsApp, Telegram, Signal, Instagram, Twitter/X, LinkedIn, Facebook Messenger and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerveband](https://clawhub.ai/user/nerveband)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to read Beeper chats, search messages, monitor unread conversations, and prepare or send messages across Beeper-connected networks. It requires Beeper Desktop API access and a valid Beeper bearer token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Beeper token exposure could allow access to all Beeper-connected networks available to the account.

Mitigation: Keep BEEPER_TOKEN out of logs and shared shell history, store it only in a trusted local environment, and rotate it if exposure is suspected.

Risk: Remote or plaintext Beeper API access can expose messages and sending authority outside the local machine.

Mitigation: Prefer localhost-only API access and avoid plaintext HTTP for remote Beeper API access.

Risk: Message sending acts with the user's account authority across connected chat networks.

Mitigation: Require the agent to show the complete draft and wait for explicit user approval before every send, reply, or forward operation.

Risk: The wrapper depends on an external Beeper CLI binary outside the artifact files.

Mitigation: Install only from a trusted source and pin or verify the external binary before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerveband/skills/beeper-api-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/nerveband)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and Beeper CLI outputs in JSON, text, or markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read chat metadata and messages, search conversations, and send messages when explicitly approved by the user.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
