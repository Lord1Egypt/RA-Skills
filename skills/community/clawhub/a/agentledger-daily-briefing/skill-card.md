## Description: <br>
Structured morning briefing skill - daily summaries covering calendar, tasks, weather, news, and priorities, with cron, heartbeat, and on-demand triggers. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[Clawdssen](https://clawhub.ai/user/Clawdssen) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
External users and agent operators use this skill to configure an agent to produce concise daily briefings from calendar, task, weather, news, and priority sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can summarize private planning data such as calendar events, tasks, email, travel, and work priorities. <br>
Mitigation: Start with on-demand briefings, grant only the data access needed for enabled sections, and review enabled sources before scheduling automated runs. <br>
Risk: Briefings may be sent to configured messaging channels where sensitive details could be visible to unintended recipients. <br>
Mitigation: Send full summaries only to private channels or direct messages, and verify channel configuration before enabling cron or heartbeat delivery. <br>
Risk: Automated cron, heartbeat, or memory-log settings can continue running or retaining details longer than intended. <br>
Mitigation: Review schedules and retention settings periodically, and disable or narrow logging when briefing history is no longer needed. <br>


## Reference(s): <br>
- [Daily Briefing advanced patterns](references/advanced-patterns.md) <br>
- [Daily Briefing release page](https://clawhub.ai/Clawdssen/agentledger-daily-briefing) <br>
- [The Agent Ledger](https://www.theagentledger.com) <br>
- [memory-os skill](https://clawhub.com/skills/memory-os) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration examples and shell-style scheduling commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefings are intended to be concise, scannable, and under 300 words unless customized.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
