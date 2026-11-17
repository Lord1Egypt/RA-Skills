## Description:

botlearn-reminder is a BotLearn 7-step onboarding guide that delivers quickstart tutorials every 24 hours and responds when users ask about BotLearn tutorial or learning progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:

MIT

## Use Case:

External BotLearn and OpenClaw users use this skill to receive daily, language-aware reminders that summarize the next BotLearn quickstart step and track completion progress across the 7-step onboarding journey.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill registers a persistent daily heartbeat that fetches BotLearn pages and writes reminder progress under OpenClaw memory.

Mitigation: Install only when that recurring BotLearn-specific behavior is acceptable, and review heartbeat registration plus memory write permissions before deployment.

Risk: The authoritative security summary reports a script injection flaw in update-progress.sh.

Mitigation: Fix update-progress.sh before use by passing values as data, validating dates, and avoiding shell interpolation into JavaScript.

## Reference(s):

- [BotLearn 7-step overview](https://botlearn.ai/7-step)
- [ClawHub skill page](https://clawhub.ai/calvinxhk/skills/botlearn-reminder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reminders with URLs, shell command snippets, and JSON progress output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily heartbeat flow; reminder summaries are expected to be concise and language-aware.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter and package.json report 0.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
