## Description:

Start every day focused. Get a morning briefing with overdue tasks, today's priorities, calendar overview, and context from recent meetings. Works with ai-meeting-notes to-do list. No setup. Just say 'briefing'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and productivity-focused teams use this skill to generate a concise morning briefing from task lists, recent meeting notes, calendar context, and memory files when available. It helps identify overdue work, today's priorities, calendar commitments, recent context, and a single focus for the day.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefing trigger phrases can cause the agent to read task lists, recent meeting notes, calendars, and memory or profile files.

Mitigation: Install only where that access is acceptable; narrow triggers or disable or confirm memory and calendar sources in shared or sensitive workspaces.

Risk: Briefings may summarize sensitive personal or business context from workspace files.

Mitigation: Review generated briefings before sharing and avoid using the skill in workspaces containing unrelated confidential notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alv-ai-daily-briefing)
- [Creator homepage](https://jeffjhunter.com)
- [Quick Start](examples/quick-start.md)
- [Example Output](examples/output-example.md)
- [Briefing Preferences](assets/PREFERENCES-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown briefing with prioritized task, calendar, context, and focus sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-message briefing; sections are skipped when source data is unavailable.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
