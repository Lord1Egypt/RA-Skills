## Description: <br>
Runs a daily task that reads clipboard and notification data from computer_io and writes a dated memory file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gift-is-coding](https://clawhub.ai/user/gift-is-coding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to combine the latest daily clipboard and notification records into a persistent dated memory markdown file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive clipboard and notification content in OpenClaw memory. <br>
Mitigation: Install only when this retention is intended, and add review or redaction steps for secrets, private messages, one-time codes, and work data. <br>
Risk: The included scheduling behavior can run the summary automatically each day. <br>
Mitigation: Review, change, or remove the scheduled cron entry before enabling the skill. <br>
Risk: The script uses a hard-coded local workspace path. <br>
Mitigation: Update the workspace path for the target environment before running it. <br>
Risk: The artifact includes contact parsing behavior beyond the basic daily summary description. <br>
Mitigation: Review or remove the contact-parsing block if collecting contact identities is not intended. <br>


## Reference(s): <br>
- [Daily Memory Summary ClawHub page](https://clawhub.ai/gift-is-coding/daily-memory-summary) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration] <br>
**Output Format:** [Markdown file with terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes memory/YYYY-MM-DD.md from the current day's latest clipboard and notification records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
