## Description: <br>
Every night, this skill scans tomorrow's calendar and sends Feishu reminders, with morning events reminded two hours in advance and afternoon events summarized at noon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Individuals use this skill to automate next-day calendar reminders from a single Outlook calendar through Feishu messages, including a nightly schedule summary and time-based reminders for upcoming events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill schedules automated calendar access and sends event details through Feishu. <br>
Mitigation: Review calendar and Feishu permissions, configure the recipient open_id carefully, and run a manual test before enabling the nightly schedule. <br>
Risk: The release describes a runtime script that is not included in the submitted artifact. <br>
Mitigation: Verify that the expected calendar_reminder.py implementation exists and matches the documented behavior before registering cron. <br>
Risk: The instructions include broad, inconsistent data-analysis trigger language outside the calendar-reminder purpose. <br>
Mitigation: Limit use to the documented calendar-reminder workflow and remove or ignore unrelated trigger language during installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/calendar-reminder-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron setup guidance, Feishu recipient configuration, reminder-rule examples, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
