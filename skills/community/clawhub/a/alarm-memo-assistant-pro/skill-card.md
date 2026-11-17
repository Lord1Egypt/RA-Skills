## Description:

A Chinese-language productivity skill for managing reminders, alarms, memos, todos, daily task summaries, and repeat schedules through available OpenClaw host capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw and ClawHub users use this skill to capture reminders, memos, todos, and daily task digests in Chinese. It helps agents turn natural-language requests into structured records, reminder drafts, and scheduled delivery plans when the host provides file, cron, session, and time tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic reminders or daily digests may not trigger if the OpenClaw host does not have active cron or session delivery.

Mitigation: Confirm cron and session delivery are enabled before relying on automatic reminders, and present unscheduled items as drafts when those capabilities are unavailable.

Risk: Reminder, memo, and todo data may be stored locally in host-managed files.

Mitigation: Confirm file locations, review saved records periodically, and delete or export local data according to the user's retention needs.

Risk: The skill cannot directly control native operating-system alarm, reminder, or notes applications without a suitable host plugin or API.

Mitigation: Disclose this limitation in responses and provide structured records or import-ready text when native integration is unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/alarm-memo-assistant-pro)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)
- [ClawHub Homepage](https://clawhub.com)
- [Cron Playbook](references/cron-playbook.md)
- [Limitations and Desktop Control](references/limitations-and-desktop-control.md)
- [Output Templates](references/output-templates.md)
- [Storage Schema](references/storage-schema.md)
- [Triggers and Routing](references/triggers-and-routing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown responses with structured reminder, memo, todo, and daily digest fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include storage locations, schedule status, delivery status, and pending confirmation items when host capabilities are limited.]

## Skill Version(s):

1.0.0 (source: release evidence and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
