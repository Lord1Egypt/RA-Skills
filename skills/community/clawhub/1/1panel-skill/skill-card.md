## Description:

Comprehensive 1Panel server management skill for AI agents. Manage Linux servers, Docker containers, databases, websites, SSL certificates, and more through 580+ API endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eaveluo](https://clawhub.ai/user/eaveluo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI agents use this skill to manage 1Panel servers, including containers, websites, databases, files, monitoring, backups, security settings, and XPack features through CLI commands or the TypeScript client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes broad server-management capabilities, including files, containers, firewall, SSH, disk, backups, and restore operations.

Mitigation: Use a least-privileged 1Panel API key and require explicit human confirmation before destructive or security-sensitive actions.

Risk: Weak connection defaults or untrusted networks can expose administrative API traffic.

Mitigation: Configure a trusted 1Panel host over HTTPS and avoid using the skill across untrusted networks.

Risk: The required ONEPANEL_API_KEY grants access to the configured 1Panel instance.

Mitigation: Store the API key in a secret manager or protected environment variable and avoid logging or sharing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eaveluo/skills/1panel-skill)
- [npm Package](https://www.npmjs.com/package/1panel-skill)
- [1Panel](https://1panel.cn/)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Shell commands, Code, Configuration instructions]

**Output Format:** [JSON API responses with Markdown, shell command, and TypeScript usage examples in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and ONEPANEL_API_KEY; commands and client calls can perform administrative actions on the configured 1Panel host.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
