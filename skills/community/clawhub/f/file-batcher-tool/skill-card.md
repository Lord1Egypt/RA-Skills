## Description:

Batch file operations for renaming, converting, organizing, counting, and inspecting files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yushimohuang](https://clawhub.ai/user/yushimohuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users managing local files use this skill to run batch rename, image conversion, file organization, duplicate discovery, file counting, and large-file listing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk operations can rename, move, overwrite, or delete many local files.

Mitigation: Use test folders first, avoid broad paths such as a home directory, keep backups, and review the command scope before execution.

Risk: Image conversion can remove original files and may overwrite converted outputs.

Mitigation: Run conversion on copies of important files and check for output filename collisions before using it on originals.

Risk: Large-file search uses user-provided size values.

Mitigation: Use explicit, narrow size values and scoped folders to reduce unintended scanning or unsafe size parsing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yushimohuang/skills/file-batcher-tool)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Markdown with inline bash code blocks and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs file-management operations on local folders and may change files in place.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
