## Description: <br>
Creates one-shot natural-language reminders for America/Bogota, emits cron job JSON, and records reminders in markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StarAtheris](https://clawhub.ai/user/StarAtheris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill to turn Spanish natural-language reminder requests into one-time scheduled cron jobs, with reminder details logged to markdown for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder contents may be sent to a fixed Telegram chat ID if ARYA_TELEGRAM_CHAT_ID is not set. <br>
Mitigation: Set ARYA_TELEGRAM_CHAT_ID to a verified chat ID that you control before installing or using the skill. <br>
Risk: Reminder text is stored locally in memory/reminders.md and scheduled into future cron jobs. <br>
Mitigation: Avoid sensitive reminder text and review scheduled jobs and local reminder logs before relying on the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/StarAtheris/arya-reminders) <br>
- [Publisher profile](https://clawhub.ai/user/StarAtheris) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Markdown, Guidance] <br>
**Output Format:** [JSON cron job request with shell invocation guidance and markdown reminder logging] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and python3; defaults to America/Bogota and supports TZ_NAME and ARYA_TELEGRAM_CHAT_ID environment overrides.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
