## Description:

Fetches English Wikipedia's "Did you know?" (DYK) facts, caches them locally, and serves them one at a time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathandeamer](https://clawhub.ai/user/jonathandeamer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to share English Wikipedia DYK facts, optionally tailor facts by topic and tone preferences, and configure recurring fact delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps a local fact cache and preference file under ~/.openclaw.

Mitigation: Use it only where local preference and served-fact history storage is acceptable, and remove ~/.openclaw/dyk-facts.json or ~/.openclaw/dyk-prefs.json when that data is no longer needed.

Risk: Automatic delivery or preference refresh can create recurring OpenClaw cron jobs.

Mitigation: Review scheduled DYK delivery and refresh jobs after setup, and remove them if recurring facts or background refresh are no longer wanted.

Risk: Facts are fetched from public English Wikipedia content and may reflect upstream changes or curation limits.

Mitigation: Treat served facts as trivia and use the included Wikipedia link to check the source article before relying on a fact in higher-stakes contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonathandeamer/skills/did-you-know)
- [Wikipedia Did You Know](https://en.wikipedia.org/wiki/Wikipedia:Did_you_know)
- [Skill homepage](https://github.com/jonathandeamer/did-you-know)
- [DYK command reference](references/commands.md)
- [DYK hook tagging guide](references/tagging-guide.md)
- [DYK tag vocabulary](references/tags.csv)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Conversational text with Wikipedia links, command-backed actions, JSON cache updates, and scheduling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses python3, the public English Wikipedia API, local files under ~/.openclaw, and optional OpenClaw cron schedules.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
