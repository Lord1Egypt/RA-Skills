## Description:

Schedule and run daily or weekly update routines for Clawdbot and installed skills through Gateway cron jobs, including update reporting and optional Clawdbot update, restart, and doctor checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xabo1986](https://clawhub.ai/user/xabo1986)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure Gateway cron jobs that check and apply updates for Clawdbot and installed skills, then report the results. It is most relevant for environments where scheduled maintenance, update summaries, and controlled restart behavior are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended scheduled jobs can update all installed skills and may optionally update and restart Clawdbot without per-update approval.

Mitigation: Prefer report-only checks or explicit approvals for changes, schedule maintenance during quiet periods, and keep rollback and provenance checks before applying updates.

Risk: The artifact includes example local paths and a fixed Telegram recipient that may not match the installing environment.

Mitigation: Replace paths, work directories, and delivery recipients with verified environment-specific values before creating the cron job.

Risk: Clawdbot self-updates and restarts can disrupt active Gateway sessions.

Mitigation: Enable self-updates only when intended, run doctor checks after updates, and review the summary report for errors or restart failures.

## Reference(s):

- [Auto-Updater (Gateway) ClawHub page](https://clawhub.ai/xabo1986/skills/auto-updater-gateway)
- [Publisher profile: xabo1986](https://clawhub.ai/user/xabo1986)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include scheduled update commands, report-only or update-and-restart posture, delivery settings, and troubleshooting notes.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
