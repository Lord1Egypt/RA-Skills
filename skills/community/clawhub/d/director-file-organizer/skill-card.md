## Description:

Automatically organize, categorize, and clean up files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[di5cip1e](https://clawhub.ai/user/di5cip1e)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize folders, categorize files by type or date, identify duplicates, rename groups of files, and plan cleanup of old or temporary files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup workflows may permanently delete old files recursively from a chosen folder.

Mitigation: Require an exact dry-run list, prefer trash or backups over permanent deletion, and avoid broad targets such as home directories or project roots.

Risk: Move, rename, or duplicate-removal actions can disrupt existing folder structures or overwrite expected names.

Mitigation: Show the proposed changes first, confirm before execution, handle name collisions explicitly, and log changes for rollback.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with file-operation plans and optional code or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include a reviewable plan before moving, renaming, or deleting files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
