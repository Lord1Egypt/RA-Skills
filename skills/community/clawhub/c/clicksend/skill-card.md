## Description:

Helps agents use ClickSend to send SMS, MMS, and voice messages and manage contacts, lists, and delivery information through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and individuals use this skill to send and manage ClickSend messages, organize contacts, and check delivery status with explicit approval for changes or sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the account routes ClickSend activity through Maton.

Mitigation: Confirm the user is comfortable with Maton as the gateway before connecting the account.

Risk: Sending messages reaches real recipients and may incur costs.

Mitigation: Confirm recipient, content, timing, and costs with the user before each send.

Risk: Triggers or destinations can continue running automated actions.

Mitigation: Create them only for specific workflows the user has approved.

## Reference(s):

- [ClickSend skill release](https://clawhub.ai/byungkyu/skills/clicksend)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [ClickSend REST API documentation](https://developers.clicksend.com/docs)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Message sends and account changes require explicit user approval.]

## Skill Version(s):

1.2.7 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
