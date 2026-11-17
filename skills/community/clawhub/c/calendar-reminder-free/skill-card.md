## Description: <br>
Helps a personal developer scan tomorrow's Outlook calendar each evening and send basic Feishu reminders for morning and afternoon events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual developers use this skill to automate a daily preview of their next-day Outlook meetings and receive Feishu reminders before morning events and at midday for afternoon events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private Outlook calendar metadata may be sent to the configured Feishu recipient. <br>
Mitigation: Confirm that the Feishu open_id is correct and that sending meeting titles, times, organizers, and locations to that recipient is acceptable before enabling scheduled reminders. <br>
Risk: A persistent daily cron entry can keep forwarding calendar details after setup. <br>
Mitigation: Review the timezone and cron registration before enabling it, and pause or remove the cron job when the reminder workflow is no longer needed. <br>
Risk: The optional sudo package installation command changes the host environment. <br>
Mitigation: Run the tzdata installation only when it is required and the system package manager is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/calendar-reminder-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May register a daily cron job and send calendar metadata to a configured Feishu recipient.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
