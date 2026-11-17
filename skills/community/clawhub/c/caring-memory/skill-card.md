## Description:

AI task reminder using priority, Ebbinghaus intervals, gamification, and active time tracking for effective task management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wukai8289](https://clawhub.ai/user/wukai8289)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent-enabled task workflow use this skill to capture tasks, generate reminders, track completions, and surface priority and Ebbinghaus review summaries from local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist user-provided task titles, descriptions, stats, and activity-pattern data in local files.

Mitigation: Install only where local task and activity records are acceptable, and review storage behavior before use.

Risk: Suggested agent integrations may automatically add, complete, or remind on tasks based on conversation text.

Mitigation: Require explicit user confirmation before auto-adding, auto-completing, or heartbeat-reminding tasks.

Risk: Stored task text may later be shown back to the agent or user without clear untrusted-content boundaries.

Mitigation: Treat task titles and descriptions as untrusted display data when rendering reminders or summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wukai8289/skills/caring-memory)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI text with example shell commands and cron-style configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists tasks, activity patterns, and gamification stats in local JSON files.]

## Skill Version(s):

2.0.0 (source: evidence.json release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
