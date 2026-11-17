## Description:

AI-powered personal secretary for task management and goal tracking. Gives you a Top 3 daily brief, captures ideas, tracks momentum, adapts to your available time and energy. Works with any model. Local-first, no data leaves your machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanglin14](https://clawhub.ai/user/yanglin14)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill as a personal productivity secretary that turns natural-language updates into local task, goal, idea, calendar, memory, and review commands. It helps the user choose a daily Top 3, track completion and skips, capture ideas, and adapt task suggestions to available time and momentum.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores tasks, goals, mood, timing data, calendar events, and inferred personal preferences in a persistent local database.

Mitigation: Review stored data periodically with the memory and long-term memory listing commands, clear sensitive entries when needed, and avoid sharing sensitive personal details unless memory behavior is changed to require consent.

Risk: Calendar integration can fetch external iCal URLs and cache event details locally, so the local-first privacy claim is qualified.

Mitigation: Only connect calendar URLs or files the user is comfortable fetching and storing locally, and disconnect calendars that should no longer be used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanglin14/skills/get-to-it)
- [Publisher profile](https://clawhub.ai/user/yanglin14)
- [Skill homepage](https://github.com/yanglin/get-to-it)
- [Persona reference](references/persona.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON-derived summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent invokes a local Python CLI that returns JSON for most commands, while morning briefs may also be emitted as Telegram Markdown.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
