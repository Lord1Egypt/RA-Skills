## Description: <br>
Monitors webpages, product prices, and competitor updates around the clock and notifies users when tracked content changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anson125chen](https://clawhub.ai/user/anson125chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor authorized webpages for price, content, or status changes, schedule recurring checks, and receive change notifications through configured channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dependency manifest may create a supply-chain risk if OpenClaw installs package.json dependencies from npm. <br>
Mitigation: Confirm OpenClaw's dependency resolution before installing; if npm installation is used, remove or replace beautifulsoup4 with a verified Python dependency path and exact pinned versions. <br>
Risk: Recurring cron checks and notifications can create ongoing network activity against monitored sites. <br>
Mitigation: Add cron entries only for intentional monitoring jobs and monitor only pages the user is authorized to watch. <br>
Risk: Telegram and email notification settings require credentials in local configuration. <br>
Mitigation: Use dedicated notification credentials and keep real tokens, passwords, and chat IDs out of version control. <br>


## Reference(s): <br>
- [Cron configuration example](crontab-example.txt) <br>
- [ClawHub release page](https://clawhub.ai/anson125chen/data-sentinel-pro-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The monitoring script prints status messages and change alerts, and stores per-URL state in local JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
