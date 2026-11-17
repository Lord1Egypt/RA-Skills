## Description:

Connects a Zalo bot to a selected chat, stores its credentials, sends a test message, and provides reminder and alert examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

Zalo bot owners and other users connect a bot to their chosen chat and set up test messages, reminders, and alerts with agent assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot token is saved in gateway configuration and may be exposed in chat history or logs.

Mitigation: Accept tokens only from the agent owner, keep them out of responses and logs, and rotate a token if exposure is suspected.

Risk: Setup restarts the gateway and sends a real message to the specified chat with limited confirmation.

Mitigation: Confirm the sender is authorized and verify the target chat before changing configuration, restarting the gateway, or sending the test message.

## Reference(s):

- [ent-zalo-connect on ClawHub](https://clawhub.ai/thinhbuiii/skills/ent-zalo-connect)
- [Zalo Bot Platform](https://bot.zaloplatforms.com)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Code]

**Output Format:** [Text and Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports connection and test-message status, including a message ID when available.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
