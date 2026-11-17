## Description:

CLI tool for managing an AI's Obsidian vault with note CRUD, bidirectional sync, capture commands, search, and intelligent resurfacing while operating locally without network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukeaustin13](https://clawhub.ai/user/lukeaustin13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to manage local Obsidian notes, capture research and conversation context, search or resurface Markdown notes, and sync selected memory content between OpenClaw memory and a vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local tool can read, write, sync, and delete Markdown files, and the security evidence says file and sync boundaries are weaker than users are told.

Mitigation: Use a backed-up test vault first and avoid delete or sync operations on important notes until path containment and confirmation behavior are reviewed.

Risk: Vault-to-memory imports can turn ordinary notes into persistent agent memory.

Mitigation: Review content before importing it from the vault and treat imported notes as durable agent memory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lukeaustin13/skills/forge-obsidian-brain)
- [README](artifact/README.md)
- [Security Model](artifact/SECURITY.md)
- [Sync README](artifact/scripts/sync/README.md)
- [Obsidian](https://obsidian.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, JSON command results, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates on local Markdown files and Obsidian vault paths; no network access is described in the supplied evidence.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
