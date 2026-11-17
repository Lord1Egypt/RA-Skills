## Description:

Multi-context memory management system for OpenClaw agents with group-isolated storage, global shared memory, workspace organization, and group-specific skills isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxwzl](https://clawhub.ai/user/wxwzl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw workspace administrators use this skill to set up persistent memory, group-isolated storage, group-specific skills, and scoped project or repository directories across private and group chat contexts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files can store sensitive chat-derived information in plaintext.

Mitigation: Do not store API keys, passwords, tokens, or sensitive personal data in memory files; use environment variables or an approved secrets manager.

Risk: Installation changes agent startup behavior by registering memory-loading instructions in AGENTS.md.

Mitigation: Require explicit administrator approval before installation in shared workspaces and review AGENTS.md changes after install or upgrade.

Risk: Group, global, private, and repository paths can be written or cloned into workspace locations.

Mitigation: Validate group identifiers, clone URLs, and destination paths; use trusted skill versions and keep group-scoped content isolated.

Risk: Shared global memory can expose information across groups.

Mitigation: Reserve global memory for non-sensitive cross-group knowledge and keep private or group-only information in the appropriate scoped memory directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wxwzl/skills/files-memory-system)
- [User Guide](references/USER_GUIDE.md)
- [Architecture](references/architecture.md)
- [Security guidance](SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell command examples and generated memory/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates workspace memory files, group directories, repository locations, and AGENTS.md registration when its scripts are run.]

## Skill Version(s):

1.16.1 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
