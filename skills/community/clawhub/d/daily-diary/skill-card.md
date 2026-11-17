## Description:

Daily Diary reviews the day's conversations, extracts key events, decisions, achievements, and insights, and generates a structured diary draft for user review and archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyu925065781](https://clawhub.ai/user/luyu925065781)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn daily conversation history into a structured personal diary draft, with prompts for review, confirmation, and archiving. It is suited for journaling workflows that need summaries, achievements, decisions, reflections, tomorrow planning, mood, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reviews private daily conversation history to produce diary content.

Mitigation: Install only when this level of conversation review is acceptable, and require user review before archiving or sending diary drafts.

Risk: The sample cron configuration may deliver diary drafts to a group chat or broadcast-style channel.

Mitigation: Before enabling automation, change delivery to a verified private owner-only destination.

Risk: Diary drafts may accidentally include sensitive information from conversations.

Mitigation: Apply the skill's sensitive data filtering guidance and omit credentials, keys, identity information, server addresses, and configuration data when uncertain.

## Reference(s):

- [Guided Prompts for Diary Entries](references/quick-prompts.md)
- [Daily Diary ClawHub Release](https://clawhub.ai/luyu925065781/skills/daily-diary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration]

**Output Format:** [Markdown diary drafts and local diary files, with optional cron job configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces first-person diary entries with summary, achievements, decisions, reflections, tomorrow plan, mood, and tags.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
