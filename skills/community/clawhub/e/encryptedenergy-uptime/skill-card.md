## Description: <br>
Monitors an OpenClaw agent with every-minute pings, a public status page, and email alerts when pings stop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmarbach](https://clawhub.ai/user/jmarbach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to configure hosted uptime monitoring for an agent and receive alerts when recurring health pings stop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring OpenClaw health and status telemetry is sent to encryptedenergy.com. <br>
Mitigation: Review the payload fields before installation and use the skill only when third-party uptime monitoring is acceptable. <br>
Risk: The setup installs persistent cron execution that runs every minute. <br>
Mitigation: Confirm the crontab entry before installing it and document how to remove the entry when monitoring is no longer needed. <br>
Risk: The API key may be placed inline in the crontab command. <br>
Mitigation: Store the key outside the crontab where possible, restrict local access to the secret, and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jmarbach/encryptedenergy-uptime) <br>
- [Encrypted Energy Homepage](https://encryptedenergy.com) <br>
- [Encrypted Energy Agent Registration](https://encryptedenergy.com/agents/new) <br>
- [Encrypted Energy Ping API](https://encryptedenergy.com/api/v1/ping) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ENCRYPTED_ENERGY_API_KEY; configured cron execution posts JSON health telemetry to encryptedenergy.com every minute.] <br>

## Skill Version(s): <br>
0.2.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
