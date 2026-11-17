## Description:

ClawConnect lets agents use one API to access Gmail, Calendar, Twitter, Slack, and Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiweil](https://clawhub.ai/user/yiweil)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect authorized personal or workspace accounts, inspect account data, and request actions such as sending Gmail, Twitter, and Slack messages through ClawConnect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected-account actions can send tweets, emails, or Slack messages from authorized accounts.

Mitigation: Require explicit confirmation before sending messages, emails, or public posts.

Risk: The skill relies on a bearer API key with access to connected third-party accounts.

Mitigation: Keep the ClawConnect API key private and review the scopes granted on ClawConnect.

## Reference(s):

- [ClawConnect service](https://clawconnect.dev)
- [ClawHub skill page](https://clawhub.ai/yiweil/skills/clawconnect)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes HTTP API examples that require a ClawConnect bearer API key.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
