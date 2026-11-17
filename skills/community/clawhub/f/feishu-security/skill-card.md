## Description:

飞书群聊安全隔离 Skill provides owner identity checks, skill installation approval, permission tiers, injection filtering, sensitive path protection, and information-isolation guidance for Feishu bot use in group chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carolyn0719](https://clawhub.ai/user/carolyn0719)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu bot operators use this skill to document and configure group-chat isolation rules, owner binding flows, guest restrictions, installation approval, and manual verification steps for shared bot environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Owner accounts receive broad powers over files, shell commands, configuration access, and skill installation.

Mitigation: Preconfigure and verify the Feishu owner ID before the bot is reachable, keep the configuration file restricted, and require runtime authorization checks before sensitive operations.

Risk: If automatic owner detection fails, first-contact binding can assign ownership to the first private-chat user.

Mitigation: Avoid deploying the bot in shared environments until a trusted owner ID is set through OpenClaw configuration or FEISHU_OWNER_ID and verified with the provided checks.

Risk: The package describes policy and validation flows but should not be treated as the sole enforcement layer for file access, shell commands, or skill installation.

Mitigation: Use platform-level access controls, audit logs, and an independent runtime authorization gate for high-impact actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carolyn0719/skills/feishu-security)
- [Publisher profile](https://clawhub.ai/user/carolyn0719)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces security operating guidance, setup commands, configuration values, and validation checklists for Feishu chat isolation.]

## Skill Version(s):

2.1.2 (source: server release metadata; artifact frontmatter lists 2.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
