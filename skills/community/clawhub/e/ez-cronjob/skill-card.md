## Description: <br>
Fix common cron job failures in Clawdbot/Moltbot - message delivery issues, tool timeouts, timezone bugs, and model fallback problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ProMadGenius](https://clawhub.ai/user/ProMadGenius) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to diagnose and fix Clawdbot/Moltbot scheduled-message failures, including delivery gaps, timeout behavior, timezone errors, and model fallback issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent or user may create persistent cron jobs with the wrong schedule, timezone, recipient, or message. <br>
Mitigation: Review job names, cron expressions, timezones, recipients, and message text before running the provided commands, then keep job IDs so unwanted jobs can be removed. <br>
Risk: Troubleshooting commands may expose private messages, chat IDs, or operational details in logs. <br>
Mitigation: Redact sensitive log content before sharing or storing diagnostic output. <br>
Risk: Shell examples can modify scheduled jobs or restart services when executed. <br>
Mitigation: Inspect each command and run only the commands that match the intended Clawdbot/Moltbot environment and recovery step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ProMadGenius/ez-cronjob) <br>
- [Clawdbot Cron Documentation](https://docs.molt.bot/tools/cron) <br>
- [Timezone Database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) <br>
- [Cron Expression Generator](https://crontab.guru/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes troubleshooting checklists and command examples for cron job setup, inspection, testing, and recovery.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
