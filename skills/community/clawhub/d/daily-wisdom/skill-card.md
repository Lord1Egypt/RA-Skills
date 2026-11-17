## Description:

Daily Wisdom helps an agent generate and deliver recurring historical anecdotes, philosophical insights, or cultural stories with original-language quotes and modern connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aytuncyildizli](https://clawhub.ai/user/aytuncyildizli)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to schedule recurring cultural and historical content through an LLM or cron-connected agent. It is suited for daily wisdom messages, morning reflections, and recurring storytelling workflows that should avoid repeated topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabled scheduled delivery can generate and send recurring content automatically.

Mitigation: Confirm the cron schedule, timezone, and destination channel before enabling the job, and disable or remove it when recurring delivery is no longer wanted.

Risk: The skill relies on a history file to avoid repeated topics.

Mitigation: Use a dedicated history file and keep it available to the agent so generated topics can be tracked across runs.

Risk: Generated historical quotes or facts may be inaccurate if not verified.

Mitigation: Use an agent with web research access and review important quotes, dates, and attributions before broad distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aytuncyildizli/skills/daily-wisdom)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [History File Template](artifact/history.md)
- [Example Outputs](artifact/examples/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown content with quote, story, modern connection, and optional cron configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append delivered topics to a local history file and may send scheduled messages through a user-configured delivery channel.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
