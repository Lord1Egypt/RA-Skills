## Description: <br>
Structured morning briefing skill for daily summaries covering calendar, tasks, weather, news, and priorities, with cron, heartbeat, and on-demand triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Clawdssen](https://clawhub.ai/user/Clawdssen) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
External users and agent operators use this skill to configure an AI agent to assemble concise daily briefings from calendar, task, weather, news, and priority inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated briefings can expose calendar, task, location, or news preferences in the configured delivery channel. <br>
Mitigation: Review the briefing configuration, enabled data sources, and channel destination before enabling cron or heartbeat delivery. <br>
Risk: Scheduled callbacks or stored configuration may continue running after setup if they are accepted without review. <br>
Mitigation: Review scheduled delivery rules and any stored configuration before accepting changes, especially for user data and external delivery destinations. <br>
Risk: News, weather, calendar, and task summaries may be incomplete or stale if integrations are unavailable. <br>
Mitigation: Test an on-demand briefing after setup and verify missing sections, timezone, and enabled integrations before relying on automated delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Clawdssen/agent-daily-briefing) <br>
- [Daily Briefing Advanced Patterns](references/advanced-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefing and setup guidance with inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefings are intended to stay concise, with standard sections for date context, weather, calendar, tasks, pending items, quick reads, and a closing line.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
