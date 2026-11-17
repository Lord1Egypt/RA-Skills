## Description:

Safely rename or migrate an OpenClaw agent by updating config and naming, migrating session content, fixing session metadata, restarting, verifying, and asking separately before deleting the old agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kid0114](https://clawhub.ai/user/kid0114)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to rename or migrate an agent while preserving session content, updating configuration and workspace naming, verifying the migrated agent, and requiring separate confirmation before deleting the old agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts handle high-impact local OpenClaw configuration, agent directories, workspace paths, and session metadata without enough input validation.

Mitigation: Review before installing or running; use only trusted, simple agent IDs, back up OpenClaw config and session data first, and patch or avoid scripts until they validate IDs, quote paths, use fixed-string or structured config checks, and prevent path traversal.

Risk: Cleanup or deletion after migration can remove old agent or session data before stability is confirmed.

Mitigation: Do not run cleanup deletion unless the user explicitly confirms it after migration is verified and backup needs are checked.

## Reference(s):

- [Agent Migration Checklist](artifact/references/checklist.md)
- [Cleanup Notes](artifact/references/cleanup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and file-operation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local shell commands and helper script usage; migration changes should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
