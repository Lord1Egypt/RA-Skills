## Description:

Project status board - compile daily status from tasks, calendar, and team updates into one dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and project leads use this skill to compile daily or on-demand project status boards from task systems, calendars, team updates, and optional delivery channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project reports can expose sensitive internal business status, workload, blockers, client details, or delivery timelines.

Mitigation: Limit allowed project sources, calendars, team members, recipients, delivery channels, and retention before deployment.

Risk: Sending status boards to Telegram, Discord, clients, or long-term archives can broaden access to sensitive project information.

Mitigation: Review recipient lists and archive locations, and treat generated reports as internal business records unless explicitly approved for external sharing.

## Reference(s):

- [DoctorClaw](https://www.doctorclaw.ceo)
- [ClawHub Skill Page](https://clawhub.ai/ceobotson-bot/skills/doctorclaw-project-status)
- [Publisher Profile](https://clawhub.ai/user/ceobotson-bot)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown status board with summary tables, prioritized actions, and optional delivery or archive instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project health labels, progress counts, workload summaries, blockers, and schedule or delivery-channel configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
