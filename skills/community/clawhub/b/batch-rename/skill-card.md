## Description:

Rename image datasets and matching annotation files with custom patterns, prefixes, suffixes, sequential numbering, preview mode, and undo support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingo-318](https://clawhub.ai/user/mingo-318)

### License/Terms of Use:


## Use Case:

Developers and dataset maintainers use this skill to rename image datasets and corresponding annotation files with sequential numbers, prefixes, suffixes, or custom patterns. It is suited to dataset cleanup workflows where users need to preview filename changes before applying them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rename operations can move files in ways that are hard to reverse if the user applies changes without checking the preview.

Mitigation: Use preview mode first and review proposed filename changes before confirming the rename.

Risk: Using --force can overwrite existing files in the target image or annotation directories.

Mitigation: Avoid --force unless an independent backup exists and filename conflicts have been checked.

Risk: The restore command depends on a .rename_backup.json file in the target directory, which can be unsafe if the directory or backup manifest is untrusted.

Mitigation: Run restore only in trusted directories with a backup manifest created and validated for that dataset.

## Reference(s):

- [Batch Rename ClawHub page](https://clawhub.ai/mingo-318/skills/batch-rename)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes preview-first usage guidance and cautions for restore and overwrite operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
