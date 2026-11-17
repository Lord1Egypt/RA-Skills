## Description:

Generate daily internship logbook drafts and weekly internship reports from GitHub and GitLab commit activity. Build Indonesian MIS-friendly summaries, prepare Telegram approval requests before submission, and install OpenClaw cron delivery for daily and weekly reporting flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mozaldy](https://clawhub.ai/user/mozaldy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and internship students use this skill to turn GitHub and GitLab commit activity into Indonesian daily logbook drafts, weekly internship reports, and approval-before-submit Telegram workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup scripts install recurring OpenClaw cron jobs and modify local scheduling state.

Mitigation: Review the generated cron jobs before relying on them, and back up HEARTBEAT.md plus crontab or OpenClaw cron configuration before setup.

Risk: The security summary identifies an unsafe executable .env configuration path.

Mitigation: Avoid running setup until .env handling is fixed, and keep any local .env file limited to trusted simple assignments.

Risk: The skill reads GitHub/GitLab activity and can deliver summaries through Telegram or a MIS submission flow.

Mitigation: Use it only in workspaces where those account reads and delivery destinations are intended, and keep the approval step before MIS submission.

## Reference(s):

- [Indonesian Logbook Formatting Guide](references/format-guide.md)
- [Repository Context Configuration](references/repo-contexts.json)
- [Daily Commit Logbook on ClawHub](https://clawhub.ai/mozaldy/skills/daily-commit-logbook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown reports, Indonesian text summaries, LaTeX report artifacts, shell commands, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write dated report files, pending MIS drafts, OpenClaw cron job configuration, and Telegram-ready approval messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
