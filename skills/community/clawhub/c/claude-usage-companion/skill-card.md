## Description: <br>
Monitors Claude programmatic credit usage with local ccusage reports, projections, and alerts, and reminds users to start their interactive Claude session at a chosen anchor time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[decisionvex](https://clawhub.ai/user/decisionvex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill on an always-on box to monitor Claude non-interactive credit usage, estimate month-end spend, receive threshold alerts, and get a human reminder to start the interactive Claude window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured alert command can execute a local shell command when alerts are delivered. <br>
Mitigation: Keep alert_command null unless a notifier is needed, review config.json carefully, and keep the skill directory writable only by trusted users. <br>
Risk: Installing the printed cron block schedules recurring local checks and reminders. <br>
Mitigation: Review the generated cron block before adding it to crontab. <br>
Risk: Usage reports estimate the programmatic credit pool from local ccusage data and may not match the exact account balance. <br>
Mitigation: Use the Usage credits line in Claude Code /usage as the authoritative remaining balance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/decisionvex/claude-usage-companion) <br>
- [ccusage](https://github.com/ryoppippi/ccusage) <br>
- [Project website](https://decisionvex.github.io/claude-usage-companion/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, status reports, cron blocks, and alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports and reminders are local; alert delivery may use a user-configured shell command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
