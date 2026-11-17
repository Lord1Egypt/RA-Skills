## Description:

EduClaw is a personal IELTS study secretary for detailed planning, Google Calendar scheduling through gcalcli, and automated study material management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moclaw](https://clawhub.ai/user/moclaw)

### License/Terms of Use:

MIT-0

## Use Case:

IELTS learners and supporting agents use this skill to create bilingual study plans, find study materials, schedule approved sessions, and track progress over a multi-month roadmap. It is intended for calendar-backed study management with local progress records and optional reminder channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions and runtime behavior can affect local dependencies and background automation.

Mitigation: Prefer isolated or pinned dependency installation, independently verify installer commands before use, and disable cron jobs unless automated reminders and reports are needed.

Risk: The skill requires credentials for Google, Discord, and optionally Telegram services.

Mitigation: Store tokens and OAuth files in protected configuration locations, restrict service permissions to the minimum needed, and rotate credentials if exposure is suspected.

Risk: Calendar write access and notification channels can create or send user-visible content.

Mitigation: Review plans before approving calendar creation, limit Google Calendar and bot permissions, and keep interactive conflict handling enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moclaw/skills/educlaw-ielts-planner)
- [README.md](artifact/README.md)
- [SETUP.md](artifact/SETUP.md)
- [WORKFLOW.md](artifact/WORKFLOW.md)
- [SQLite schema](artifact/schema.sql)
- [OpenClaw](https://openclaw.dev)
- [gcalcli](https://github.com/insanum/gcalcli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with calendar-event text, shell commands, and local tracker file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces study plans, event descriptions, reminder/report prompts, and local Markdown or SQLite tracking updates when configured.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
