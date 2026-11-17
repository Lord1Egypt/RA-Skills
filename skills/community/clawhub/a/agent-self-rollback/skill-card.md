## Description:

Deploys a portable self-rollback workflow for AI agents to snapshot, verify, list, and restore their own persistent memory files and selected project files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mowenqwq](https://clawhub.ai/user/mowenqwq)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent maintainers use this skill to add snapshot and rollback procedures around agent memory files such as identity, user profile, facts, and journals. It is also useful when an agent needs lightweight protection before modifying selected project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The rollback workflow can overwrite durable agent memory or selected project files during restore.

Mitigation: Inspect the selected snapshot before restore, require explicit confirmation, and keep the pre-restore backup behavior enabled.

Risk: Snapshots can preserve sensitive memory content or secrets if scoped too broadly or stored in an exposed location.

Mitigation: Configure an explicit absolute agent data directory, limit protected paths to intended files, keep the snapshots directory private, and avoid snapshotting secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mowenqwq/skills/agent-self-rollback)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Rollback Script](artifact/scripts/rollback.ps1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell and batch command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configurable file paths, snapshot commands, restore confirmation behavior, and verification steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
