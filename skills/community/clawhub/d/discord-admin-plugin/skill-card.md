## Description:

Full Discord server administration suite for OpenClaw: roles, moderation, channels, invites, webhooks, audit log, and member management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rendrag-git](https://clawhub.ai/user/rendrag-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Discord server operators use this skill to administer Discord servers from OpenClaw, including role changes, moderation actions, channel configuration, invites, webhooks, audit logs, and member lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform destructive Discord administration actions, including bans, message deletion, role changes, channel permission changes, and webhook or invite deletion.

Mitigation: Require human confirmation before destructive actions and install the skill only where this full administration surface is needed.

Risk: Webhook URLs may be exposed in tool outputs.

Mitigation: Avoid exposing outputs to untrusted users and rotate any webhook URLs that may have been revealed.

Risk: A broad Discord bot token can grant more server control than the use case requires.

Mitigation: Use a dedicated Discord bot with the smallest required permissions and restrict it to intended servers.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON serialized in text tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include success or error status and action-specific Discord administration data.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
