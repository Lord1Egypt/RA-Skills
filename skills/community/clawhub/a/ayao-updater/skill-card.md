## Description:

Automatically updates OpenClaw and installed ClawHub skills on a configurable schedule, handling package manager detection, local changes, release channels, and notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayao99315](https://clawhub.ai/user/ayao99315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining OpenClaw environments use this skill to configure scheduled or manual updates for OpenClaw and installed ClawHub skills. It is suited for managing update cadence, skip lists, pre-release filtering, gateway restarts, and update notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent user-level cron updater that can automatically change OpenClaw and installed skills.

Mitigation: Run manual dry runs first, avoid installing it as root, review the configured schedule, and keep skip lists current for skills that should not be changed automatically.

Risk: Release evidence reports unsafe cron and configuration handling that could be abused for persistent command execution.

Mitigation: Keep the configuration file private and trusted, and review or fix cron schedule validation, config path handling, and log-file location before enabling unattended updates.

Risk: Automated updates can introduce breaking changes or failed skill updates without immediate operator review.

Mitigation: Use pre-release filtering, monitor the update log and notifications, and rely on local-change detection plus explicit skip lists for skills that require manual review.

## Reference(s):

- [Ayao Updater ClawHub page](https://clawhub.ai/ayao99315/skills/ayao-updater)
- [Config Schema](references/config-schema.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with Bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide use of local scripts that install or remove a cron job, run update checks, update OpenClaw and ClawHub skills, restart the gateway, write logs, and send notifications.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
