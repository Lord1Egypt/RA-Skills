## Description:

A general-purpose file organization skill that sorts files by type, size, date, and keywords for workflows such as downloads cleanup, photo archiving, and document classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate and execute file-sorting workflows for local folders, including organizing files into type, size, or date-based output directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Undo and overwrite behavior can cause unexpected file loss or movement.

Mitigation: Review before installing, use preview first, avoid output directories with valuable overlapping filenames, do not run undo when the hidden backup file may have been modified by other users or untrusted processes, and do not run with elevated privileges.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file move, copy, symlink, preview, and undo operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-03-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
