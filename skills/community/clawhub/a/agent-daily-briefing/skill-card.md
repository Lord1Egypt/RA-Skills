## Description:

Structured morning briefing skill - daily summaries covering calendar, tasks, weather, news, and priorities, with cron, heartbeat, and on-demand triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

External users and agent operators use this skill to configure an AI agent that prepares concise morning briefings from calendar, weather, task, pending-item, news, and priority context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings may summarize personal calendar, task, location, pending-item, and optional news context into messaging channels.

Mitigation: Configure BRIEFING.md with private delivery channels, disable sections that are not needed, and avoid shared Discord or Telegram destinations for personal data.

Risk: Advanced briefing analytics or memory logging can persist briefing history that contains sensitive personal or work context.

Mitigation: Enable persistent memory logging only when briefing history is desired, and review workspace access and retention expectations before use.

Risk: Weather, calendar, task, and news sections depend on the agent's connected tools and integrations and may be incomplete if those sources are unavailable.

Mitigation: Test an on-demand briefing after setup, verify configured integrations, and disable sections that cannot be reliably sourced.

## Reference(s):

- [Daily Briefing Advanced Patterns](references/advanced-patterns.md)
- [Agent Daily Briefing on ClawHub](https://clawhub.ai/clawdssen/skills/agent-daily-briefing)
- [The Agent Ledger](https://www.theagentledger.com)
- [memory-os dependency](https://clawhub.com/skills/memory-os)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing guidance with configuration snippets and optional shell-style scheduling commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefings are intended to be concise, scannable, and typically under 300 words.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
