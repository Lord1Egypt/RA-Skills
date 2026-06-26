## Description: <br>
A reminder and memo management skill that helps agents organize alarms, reminders, todos, daily task summaries, recurring reminders, and structured fallback records when host scheduling or storage tools are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to capture reminders, memos, todos, and daily task digests, with structured outputs for storage and scheduling when the host environment supports those capabilities. It is especially suited for personal productivity workflows that need clear confirmation of what was recorded, scheduled, or left as a draft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store reminder, memo, todo, and daily digest content locally. <br>
Mitigation: Confirm where data files are stored and how records can be reviewed, edited, disabled, or deleted before enabling persistent workflows. <br>
Risk: Recurring reminders and daily pushes depend on host scheduling and message-delivery capabilities. <br>
Mitigation: Only describe reminders as scheduled after the host confirms cron or session delivery setup; otherwise present them as drafts or manually refreshable summaries. <br>
Risk: Users may expect direct control over native operating system alarm or notes applications. <br>
Mitigation: State when native app integration is unavailable and provide structured records or importable text as the fallback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/alarm-memo-assistant-pro) <br>
- [ClawHub homepage](https://clawhub.com) <br>
- [README](artifact/README.md) <br>
- [Cron Playbook](artifact/references/cron-playbook.md) <br>
- [Limitations and Desktop Control](artifact/references/limitations-and-desktop-control.md) <br>
- [Storage Schema](artifact/references/storage-schema.md) <br>
- [Output Templates](artifact/references/output-templates.md) <br>
- [Triggers and Routing](artifact/references/triggers-and-routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with structured reminder, memo, todo, and daily digest sections; may include JSON-shaped storage records or cron schedule details when supported by the host.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should clearly distinguish created records from drafts and list any missing confirmations or unavailable host capabilities.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
