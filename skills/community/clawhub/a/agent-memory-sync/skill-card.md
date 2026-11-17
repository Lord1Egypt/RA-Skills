## Description:

Preserves, searches, reviews, and exports user-owned agent memory across OpenClaw, Codex, Claude, OpenCode, Hermes, Qoder, Obsidian, and Git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wildprogrammer](https://clawhub.ai/user/wildprogrammer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Memory Sync to preserve local agent memory, chat stores, and handoff summaries, then review them into durable Obsidian memory indexes, profile/context packs, skill inventories, and optional Git-synced outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can archive raw agent conversations, tool outputs, rule files, profile data, project metadata, and skill inventories into an Obsidian vault.

Mitigation: Install only when this local copying behavior is acceptable, keep the vault private, and review generated Sources and review packs before sharing or syncing.

Risk: Archived memory data can be staged for Git and may expose sensitive material if pushed to an unintended remote.

Mitigation: Leave GIT_PUSH_ENABLED=false unless the remote repository is private and intended for this data, and confirm repository visibility before enabling push.

Risk: Conversation scans may preserve credentials, customer data, private keys, or regulated information if those appear in local agent stores.

Mitigation: Avoid scanning conversations that may contain those data classes, and do not store secrets or regulated material as durable memory.

Risk: Cleanup can permanently delete Obsidian source copies when delete mode is explicitly enabled.

Mitigation: Use the default trash cleanup mode for normal operation and enable permanent deletion only when intentional.

## Reference(s):

- [Memory Sync GitHub repository](https://github.com/Wildprogrammer/memory-sync-skill)
- [Memory Sync ClawHub skill page](https://clawhub.ai/wildprogrammer/skills/agent-memory-sync)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Obsidian vault content, memory indexes, context/profile packs, skill inventories, and optional Git sync guidance.]

## Skill Version(s):

1.0.3 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
