## Description:

Automates daily health checks, fixes, memory cleanup, backups, improvements, upgrades, and security audits for the OpenClaw environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install scheduled maintenance jobs for diagnostics, remediation, cleanup, backups, upgrade checks, and security audits. It is intended for environments where recurring access to OpenClaw configuration, workspace state, logs, gateway controls, Git repositories, and Slack notifications has been reviewed and approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended maintenance jobs can copy secrets, mutate repositories, delete logs, restart services, and send operational details to Slack.

Mitigation: Review every scheduled job before installation, and disable or edit backup, Git commit, log deletion, restart, and Slack notification behavior unless explicitly approved.

Risk: Backups can include OpenClaw configuration and .env files.

Mitigation: Exclude secrets or require encryption, restricted access, and retention controls before allowing backups to copy sensitive files.

Risk: Slack notifications can disclose operational paths, status, and security audit details.

Mitigation: Use restricted Slack channels or webhooks and redact sensitive paths or status details before enabling notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/skills/evomasterscheduler)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation and Bash/Zsh scripts that install cron jobs, write log text, and send operational notifications.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates recurring OpenClaw maintenance tasks and daily log output under the user's OpenClaw log directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
