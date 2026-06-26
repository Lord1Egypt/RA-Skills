## Description: <br>
A background agent that generates a daily life prediction by analyzing local data and social signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Invelene](https://clawhub.ai/user/Invelene) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to run a local, unattended daily agent that reads personal calendar, messaging, recent file, and logged-in social context to produce a desktop life prediction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to run unattended while reading private messages, calendar events, recent files, and logged-in social pages. <br>
Mitigation: Run it manually or in an isolated local-only session, disable memory and logging, and grant only the data permissions required for the intended run. <br>
Risk: Browser-cookie social scraping and Full Disk Access can expose sensitive account and local message data. <br>
Mitigation: Disable social-cookie scraping unless explicitly needed, avoid Full Disk Access where possible, and require each notification to state which data categories were used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Invelene/daily-oracle) <br>
- [Publisher profile](https://clawhub.ai/user/Invelene) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Desktop notification text with supporting setup guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The primary agent-facing result is a single prediction notification; setup guidance includes cron scheduling and local permission requirements.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
