## Description:

Discord community management helper for ClawLink OAuth workflows, covering guild queries, member permissions, application command permissions, subscriptions, entitlements, and role connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Community operators and Discord application developers use this skill to inspect Discord guild, member, authorization, entitlement, subscription, and role-connection state, and to prepare controlled changes that require explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests local read/write/exec authority that is broader than its Discord OAuth workflow appears to need.

Mitigation: Review the skill before installation and enable local filesystem or command execution authority only where that authority is acceptable for the deployment environment.

Risk: Some Discord operations can leave a guild, delete or consume entitlements, change profile data, or update role-connection metadata.

Mitigation: Require explicit confirmation for guild leave, entitlement deletion or consumption, profile changes, and role-connection updates, with a second confirmation for high-impact actions.

Risk: Invocation metadata includes inconsistent database or SQL wording that does not match the Discord OAuth workflow.

Mitigation: Treat the skill as applicable only to Discord OAuth and community-management workflows, and ignore database or SQL invocation text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-community-hub)

## Skill Output:

**Output Type(s):** [guidance, api calls, code, shell commands, configuration]

**Output Format:** [Markdown with tables, JavaScript examples, and shell configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discord changes are separated into safe, confirm, and high-impact actions; high-impact actions require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
