## Description:

Daily Backup helps an agent check its current workspace for pending Git changes and decide whether to commit and push them on a daily schedule or by manual request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain Git backups of an agent workspace, inspect change status, and coordinate commits and pushes to a private remote repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can commit and push workspace data, which may expose sensitive files if workspace scope is loose.

Mitigation: Use only with a private, access-controlled remote, require AGENT_WORKSPACE to be explicitly set, and review exact staged files before scheduled backups run.

Risk: Scheduled backups may capture secrets, generated artifacts, or files that should not be versioned.

Mitigation: Maintain a .gitignore or allowlist and run secret scanning before any commit or push.

## Reference(s):

- [Remote repository setup guide](artifact/references/spec.md)
- [ClawHub skill page](https://clawhub.ai/axelhu/skills/daily-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with shell-command guidance and status lines from the pre-flight script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Git repository status, change counts, and up to 30 changed file entries.]

## Skill Version(s):

1.9.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
