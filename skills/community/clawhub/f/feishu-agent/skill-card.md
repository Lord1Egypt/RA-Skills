## Description:

Feishu Agent is a Feishu (Lark) CLI agent that provides calendar, todo, and contact management capabilities for AI assistants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boyd4y](https://clawhub.ai/user/boyd4y)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI assistant operators use this skill to configure a Feishu app, authenticate with OAuth 2.0, and issue CLI commands for calendar scheduling, todo management, and contact lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unreviewed mutable CLI package.

Mitigation: Use only a pinned and trusted CLI release, and avoid mutable bunx latest execution for sensitive Feishu accounts.

Risk: Feishu app secrets and OAuth tokens may be stored in plaintext at ~/.feishu-agent/config.json.

Mitigation: Protect the config file, prefer environment variables where practical, and confirm that configuration output redacts secrets before sharing logs.

Risk: Calendar deletes and todo updates can make real changes in a Feishu account.

Mitigation: Grant the narrowest Feishu permissions needed and confirm destructive or account-changing commands before execution.

## Reference(s):

- [ClawHub Feishu Agent Skill Page](https://clawhub.ai/boyd4y/skills/feishu-agent)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the bun runtime; commands may read from and write to the user's Feishu account after authentication.]

## Skill Version(s):

1.0.14 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
