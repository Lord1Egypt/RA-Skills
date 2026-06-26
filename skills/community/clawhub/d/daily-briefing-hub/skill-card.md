## Description: <br>
Daily Briefing Hub produces a prioritized daily briefing that combines calendar events, email highlights, weather, GitHub activity, tasks, and news for delivery through configured channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ariktulcha](https://clawhub.ai/user/ariktulcha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to collect schedule, inbox, task, development, weather, and news signals into a concise morning briefing or evening recap. It is also used to configure recurring briefings delivered through channels such as Telegram, Slack, WhatsApp, or Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally reads sensitive connected-account data such as calendars, email, tasks, development activity, location, feeds, delivery channels, and briefing preferences. <br>
Mitigation: Use least-privilege account permissions, choose private delivery channels, confirm any recurring cron schedule, and periodically review stored briefing preferences. <br>


## Reference(s): <br>
- [Daily Briefing Hub on ClawHub](https://clawhub.ai/ariktulcha/daily-briefing-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefing with optional JSON cron configuration and channel delivery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sections are adapted to available connected tools and omit empty sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
