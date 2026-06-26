## Description: <br>
Automates CPMO morning reports and evening summaries by reading live Apple Notes, Calendar, reminders, and local ledger data, then syncing daily report records to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AyangAI](https://clawhub.ai/user/AyangAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project and operations leads use this skill to assemble daily priorities, evening progress summaries, risk alerts, and overdue task follow-up from live local work data. It is configured to archive daily report records to a Feishu base after checking whether a same-day record already exists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill repeatedly reads sensitive local work data from Apple Notes, Calendar, reminders, and local ledgers. <br>
Mitigation: Confirm the named data sources are intended for this workflow and add review or redaction rules for sensitive notes, meetings, reminders, risks, and pending items. <br>
Risk: The skill syncs daily summaries to a fixed Feishu destination. <br>
Mitigation: Verify the Feishu base belongs to the user or organization and review what will be included before enabling automated sync. <br>
Risk: Cron automation can generate and send reports on a schedule with limited user controls. <br>
Mitigation: Require approval for sensitive report content and validate the configured schedule before enabling unattended operation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AyangAI/cpmo-daily-report) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, inline shell and AppleScript commands, and JSON cron configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for scheduled 08:00 morning reports and 17:30 evening summaries using real-time source reads.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
