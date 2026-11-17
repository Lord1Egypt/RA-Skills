## Description:

Automatically update OpenClaw and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitchegumi](https://clawhub.ai/user/gitchegumi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure unattended daily OpenClaw and skill/plugin updates, service restarts, and update summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent unattended daily updates for OpenClaw code, installed skills, and plugins.

Mitigation: Install only when unattended updates are intended; prefer check-and-notify behavior, pinned or trusted sources, audit logs, and rollback procedures.

Risk: The update flow restarts a system service with sudo.

Mitigation: Use a narrowly scoped sudoers rule for only the required restart command and do not grant broad passwordless sudo to the Gateway user.

## Reference(s):

- [OpenClaw Updating Guide](https://docs.openclaw.ai/cli/update)
- [Cron Jobs](https://docs.openclaw.ai/cron)
- [ClawHub skill page](https://clawhub.ai/gitchegumi/skills/auto-updater-sxdg2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, manual update, troubleshooting, and status-summary guidance for OpenClaw auto-updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
