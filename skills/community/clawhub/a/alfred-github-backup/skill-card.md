## Description:

Backs up an OpenClaw workspace to a private GitHub repository and guides setup for manual backups, scheduled backups, status checks, and restore steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziqi-jin](https://clawhub.ai/user/ziqi-jin)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and workspace maintainers use this skill to configure GitHub-based backups, trigger manual backups, schedule recurring backups, inspect backup status, and follow restore steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub credentials could be exposed if pasted into chat or embedded in a remote URL.

Mitigation: Use GitHub CLI, SSH, a credential helper, or a fine-grained repository-specific token stored outside the conversation.

Risk: Backups may include sensitive workspace memory, configuration, or user information.

Mitigation: Review staged files before pushing, add exclusions for secrets, and enable secret scanning on the destination repository.

Risk: Restore steps can overwrite existing workspace files.

Mitigation: Restore into a temporary directory first, compare changes, and copy only the files that should replace the current workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziqi-jin/skills/alfred-github-backup)
- [Publisher profile](https://clawhub.ai/user/ziqi-jin)
- [GitHub token settings](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided GitHub account, repository name, backup schedule, and credential method.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
