## Description:

Enables multi-Agent collaboration on Feishu by relaying tasks between coordinator and specialist Bots with user ID mapping and proactive messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glassmarbles](https://clawhub.ai/user/glassmarbles)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to configure Feishu coordinator and specialist Bots that relay tasks, resolve Bot-specific open_id mappings, and send proactive specialist messages to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual user ID entry in multi-user mode can allow spoofed or mistaken identities.

Mitigation: Use the skill only in a tightly controlled internal workspace and add SSO, LDAP, or another verified identity source before production use.

Risk: The user mapping file stores sensitive routing identifiers and can be overwritten if file access is weak.

Mitigation: Protect user-mapping.json with restrictive permissions, limit write access to trusted Bots, and move to authenticated storage with audit logging for team or production deployments.

Risk: Single-user mode can be misused if the Bots are shared beyond the intended owner.

Mitigation: Restrict Bot visibility to the intended user and lock registration to a verified owner open_id.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glassmarbles/skills/feishu-agent-relay)
- [Feishu Bot Setup Guide](references/feishu-bot-setup.md)
- [Single-User Mode Setup Guide](references/single-user-setup.md)
- [User Mapping Table Schema](references/mapping-schema.md)
- [Relay Examples](references/relay-examples.md)
- [Feishu Developer Console](https://open.feishu.cn/)
- [Feishu App Console](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript examples, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a mapping API script and setup references for single-user and multi-user Feishu Bot deployments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
