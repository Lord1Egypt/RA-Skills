## Description: <br>
Generates a warm, compact daily briefing with weather, calendar, reminders, birthdays, and important emails for cron or chat delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antgly](https://clawhub.ai/user/antgly) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to generate a short daily briefing from local weather, calendar, reminders, birthdays, contacts, and email context for interactive use or scheduled delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect sensitive personal data from calendar, reminders, contacts, birthdays, and email integrations. <br>
Mitigation: Enable only the integrations needed for the deployment and review the skill before installing, especially on shared machines or automated setups. <br>
Risk: The generated data file can leave a consolidated copy of sensitive briefing inputs in /tmp/daily_briefing_data.json. <br>
Mitigation: Clean up or restrict access to /tmp/daily_briefing_data.json after use and treat cron logs or chat transcripts as sensitive. <br>
Risk: Mail configuration may involve credentials such as an iCloud app-specific password. <br>
Mitigation: Avoid storing mail passwords in plain configuration where possible and keep the important-email integration disabled unless needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/antgly/daily-briefing) <br>
- [Publisher Profile](https://clawhub.ai/user/antgly) <br>
- [README.md](artifact/README.md) <br>
- [wttr.in Weather API](https://wttr.in/:help) <br>
- [Apple App-Specific Passwords](https://support.apple.com/en-us/HT204397) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text daily briefing with lightweight Markdown bullets and headings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for cron or chat delivery; requires macOS with bash and curl, with optional calendar, reminders, contacts, and email integrations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
