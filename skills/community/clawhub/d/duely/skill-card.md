## Description:

Track recurring maintenance tasks from the command line. Use when scheduling, checking, and logging periodic tasks like backups, reviews, or any repeating chore. Shows overdue items and keeps an execution log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halbotley](https://clawhub.ai/user/halbotley)

### License/Terms of Use:


## Use Case:

Developers and operators use duely to schedule recurring maintenance tasks, check what is due or overdue, and log completed or skipped work from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party Homebrew package.

Mitigation: Install only when the halbotley Homebrew tap is trusted or the duely package has been independently verified.

Risk: The remove command may delete local task data, and recoverability is not described in the artifact.

Mitigation: Review the selected task ID before removal and keep backups of local duely data when task history matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halbotley/skills/duely)
- [Publisher profile](https://clawhub.ai/user/halbotley)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include duely CLI commands for adding, listing, checking, running, skipping, logging, or removing local recurring tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
