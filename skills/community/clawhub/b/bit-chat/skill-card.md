## Description:

Payment rails between humans and AI agents via BitChat, with guidance for messaging-based Bitcoin payments and mailbox setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eliaspfeffer](https://clawhub.ai/user/eliaspfeffer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let agents request a Bit-Chat Lightning address, send or request Bitcoin over supported messenger channels, check balances, and create a persistent Bit-Chat email mailbox when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to contact Bit-Chat, create or use a mailbox, poll messages, and handle Bitcoin or bank-related instructions.

Mitigation: Require explicit human approval before setup, every outbound message, every payment, buy, sell, or top-up action, and any bank-detail sharing.

Risk: Mailbox setup requires credentials that could be lost or exposed if kept only in chat context or stored carelessly.

Mitigation: Use a password manager, OS keychain, or team secret store where available, and keep any local fallback file non-public and gitignored.

Risk: Repeated sending to invalid or unwanted recipients can cause delivery failures or SMTP suspension.

Mitigation: Verify recipients before sending, keep outbound volume low, avoid unsolicited bulk outreach, and stop for human review after repeated delivery failures.

Risk: Payment, top-up, and bank-detail workflows can route funds or account details to the wrong channel if identifiers are mixed up.

Mitigation: Confirm the platform, recipient identifier, transaction note, and intended account owner with the human before sharing details or initiating payment-related actions.

## Reference(s):

- [ClawHub Bit Chat Skill](https://clawhub.ai/eliaspfeffer/skills/bit-chat)
- [Bit-Chat Homepage](https://bit-chat.me)
- [Bit-Chat Skill Instructions](https://bit-chat.me/skill.md)
- [Create Email Skill](https://bit-chat.me/create-email-skill.md)
- [Bit-Chat Heartbeat](https://bit-chat.me/heartbeat.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with example messages, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to contact external messaging channels, create or use mailbox credentials, poll messages, and coordinate Bitcoin or bank-related actions.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
