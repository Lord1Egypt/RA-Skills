## Description:

AutoThread lets an agent turn messages that start with `/topic` into Telegram or Nicegram forum topics, Discord public threads, or Signal titled digest messages, using generated titles and platform-specific adapter scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abyssbugg](https://clawhub.ai/user/abyssbugg)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to create organized topic or thread follow-ups from group messages across Telegram, Nicegram, Discord, and Signal. It is intended for configured messaging workspaces where platform bot credentials and group permissions are managed by the operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-bearing API calls are made using bot tokens or Signal account settings read from the local OpenClaw configuration.

Mitigation: Install only in environments where the OpenClaw configuration is protected, and use bots or accounts with permissions limited to the groups or servers where `/topic` should operate.

Risk: `/topic` reposts message content and sender attribution into a new topic, thread, or Signal digest that may be visible to a broader audience.

Mitigation: Avoid invoking the skill on sensitive messages, keep mention requirements enabled in busy or public Telegram groups, and deploy only where repost visibility is acceptable.

Risk: The runtime can override platform API endpoints through `AUTOTHREAD_API_BASE`, which could redirect credential-bearing requests if misconfigured.

Mitigation: Ensure the runtime environment cannot set arbitrary `AUTOTHREAD_API_BASE` values, or prefer an updated release that validates or removes API endpoint overrides.

Risk: The security scan classifies the release as suspicious because of credential-bearing API calls and broad direct tool access.

Mitigation: Review before installing, scan the skill before deployment, and prefer a future release that narrows direct tool permissions.

## Reference(s):

- [AutoThread homepage](https://github.com/abyssbugg/autothread)
- [OpenClaw](https://openclaw.ai)
- [Discord Developer Portal](https://discord.com/developers)
- [signal-cli](https://github.com/AsamK/signal-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and adapter JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapter scripts return JSON containing topic_id, title, and link when a platform operation succeeds.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
