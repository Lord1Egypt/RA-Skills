## Description:

Advanced filesystem operations for listing files, searching content, batch processing, and directory analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vetas67](https://clawhub.ai/user/vetas67)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill as a filesystem command reference for listing directories, searching by name or content, analyzing file sizes and structure, and preparing batch copy, move, rename, or delete operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch copy, move, delete, rename, or replace examples can affect many local files if run against the wrong path.

Mitigation: Preview affected files, confirm the target directory, prefer dry-run or listing commands first, and back up important data before destructive operations.

Risk: Commands run outside a project workspace may expose or modify sensitive local files.

Mitigation: Restrict commands to the intended workspace and review paths carefully before executing operations outside that scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vetas67/skills/filesystem-1-0-0)
- [Publisher profile](https://clawhub.ai/user/vetas67)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language command reference with safety guidance for local filesystem operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
