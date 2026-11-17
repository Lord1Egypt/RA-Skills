## Description:

Guides agents on how to create real Feishu @ mentions by using post rich text messages with at tags and the correct user_id or open_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lens-lzy](https://clawhub.ai/user/lens-lzy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when composing Feishu messages that must notify a specific person. It explains why plain @ text is insufficient and gives the expected rich text message structure plus ways to obtain the needed user identifier.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to access Feishu user identifiers from group members or message mentions.

Mitigation: Use it only with Feishu integrations that are authorized to access and use that identity information.

Risk: Plain @ text may be mistaken for a real notification mention.

Mitigation: Use Feishu post rich text messages with at tags and a valid user_id or open_id when a real mention is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lens-lzy/skills/feishu-easy-at)
- [ClawHub publisher profile](https://clawhub.ai/user/lens-lzy)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Code]

**Output Format:** [Markdown guidance with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu post message JSON examples and identifier lookup guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
