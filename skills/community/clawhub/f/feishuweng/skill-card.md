## Description:

Sends text messages through configurable Feishu apps using App ID and Secret authentication and a provided or default recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wengjianmin19850412](https://clawhub.ai/user/wengjianmin19850412)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent send text notifications or user-supplied messages to a configured Feishu user or group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text and recipient identifiers are sent to Feishu through configured app credentials.

Mitigation: Use only approved Feishu workspaces and avoid sending secrets or regulated information unless approved for that workspace.

Risk: The skill can send messages to a caller-provided recipient or a configured default recipient.

Mitigation: Bind credentials and default recipients per agent, and restrict callers that are allowed to provide recipient IDs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wengjianmin19850412/skills/feishuweng)
- [ClawHub publisher profile](https://clawhub.ai/user/wengjianmin19850412)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Feishu API response object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the raw Feishu API response for the message-send request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
