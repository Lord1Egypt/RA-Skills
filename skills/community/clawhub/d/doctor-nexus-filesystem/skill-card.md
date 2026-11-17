## Description:

Perform advanced filesystem tasks including recursive listing, name and content searching, batch copying, moving, deleting, and directory size and type analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srikanth-hn](https://clawhub.ai/user/srikanth-hn)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to guide filesystem inspection, search, cleanup, batch file operations, and directory analysis workflows through shell-command examples and safety reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch copy, move, delete, or rename commands can affect many files at once or remove files irreversibly.

Mitigation: Confirm the target directory and file list before execution, prefer dry runs or backups, and review destructive commands before running them.

Risk: Filesystem commands may target sensitive system directories or require elevated permissions.

Mitigation: Avoid sudo and system directories unless that level of access is explicitly intended and the scope has been confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/srikanth-hn/skills/doctor-nexus-filesystem)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes filesystem operation examples and safety guidance for reviewing targets before batch edits, moves, or deletes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
