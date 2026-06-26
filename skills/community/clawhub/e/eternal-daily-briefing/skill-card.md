## Description: <br>
Generates a consolidated daily briefing with weather, calendar events, tasks, news, and market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eternal0404](https://clawhub.ai/user/eternal0404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agent operators use this skill to generate morning briefings or scheduled daily digests that combine external live data with local task and event files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local briefing, task, and event files that may contain personal context. <br>
Mitigation: Review the configured ~/.briefing paths and stored task/event data before enabling the skill. <br>
Risk: Broad trigger phrases and cron usage may cause the briefing to run unintentionally. <br>
Mitigation: Configure the skill to run only on explicit commands unless the scheduler and command are intentionally enabled. <br>
Risk: Weather, news, and market sections depend on external live data providers that may be unavailable, delayed, or inaccurate. <br>
Mitigation: Treat briefing output as informational and verify important decisions against primary sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eternal0404/eternal-daily-briefing) <br>
- [Publisher profile](https://clawhub.ai/user/eternal0404) <br>
- [wttr.in weather endpoint](https://wttr.in/{location}?format=j1) <br>
- [Google News RSS endpoint](https://news.google.com/rss/search?q={topic}&hl=en&gl={region}&ceid={region}:en) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Formatted text briefing, compact single-line text, or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports full briefing output, section-specific output, short mode, and machine-readable JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
