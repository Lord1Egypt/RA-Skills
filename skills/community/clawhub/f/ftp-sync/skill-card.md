## Description:

FTP/SFTP sync tool for synchronizing files between local and remote servers, with documented support for incremental backup, sync reports, and key authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and server administrators use this skill to generate or run commands for comparing local and remote directories and planning FTP/SFTP upload or download workflows for website maintenance and server management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script is mostly placeholder behavior while the documentation presents it as an FTP/SFTP sync and backup tool.

Mitigation: Treat the skill as nonfunctional until documentation and implementation are aligned and remote sync behavior has been tested.

Risk: The documented commands pass server passwords on the command line.

Mitigation: Avoid pasting real server passwords into commands; use safer authentication and secret handling before deployment.

Risk: Users may rely on the skill for backups or deployments despite the security verdict warning.

Mitigation: Review before installation and do not rely on it for backups or deployments in its current form.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/ftp-sync)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and Python code guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command-line options for host, user, password, remote path, sync mode, and dry-run behavior.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
