## Description:

Perform safe, auditable file operations with path validation and backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when an agent needs to read, write, update, delete, move, or copy workspace files with path checks, backups, and explicit reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed trigger metadata may make activation scope unclear for a skill that can change or delete files.

Mitigation: Review and correct trigger metadata before installation, and require explicit, narrow activation rules.

Risk: File operations can overwrite, move, or delete workspace content when used with broad path access.

Mitigation: Limit execution to intended workspace paths, print resolved paths before action, and keep backups enabled for overwrite or delete operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/axodus-file-operations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured YAML status examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports operation, affected paths, backup paths, result, and notes.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
