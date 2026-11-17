## Description:

Structured morning briefing skill - daily summaries covering calendar, tasks, weather, news, and priorities. Supports cron, heartbeat, and on-demand triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

External users and developers use this skill to have an agent assemble and deliver a concise morning briefing from configured calendar, task, weather, news, and priority sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to read privacy-sensitive calendar, task, location, optional news, inbox, and memory sources.

Mitigation: Keep BRIEFING.md narrowly scoped, avoid sensitive details where possible, and connect only the sources needed for the desired briefing.

Risk: Scheduled cron or heartbeat delivery may send briefings automatically to a configured messaging channel.

Mitigation: Review automation settings and channel configuration before enabling unattended delivery.

Risk: Optional briefing analytics or memory logging can create persistent records of briefing history and task status.

Mitigation: Enable logging only when persistent briefing history is intended, and review retention expectations for the workspace.

## Reference(s):

- [Daily Briefing Advanced Patterns](references/advanced-patterns.md)
- [memory-os dependency](https://clawhub.com/skills/memory-os)
- [The Agent Ledger](https://www.theagentledger.com)
- [ClawHub skill page](https://clawhub.ai/clawdssen/skills/agentledger-daily-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing text with optional configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefings are intended to be concise and scannable, typically under 300 words.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
