## Description:

This skill helps agents query locally synced Apple Health, live heart-rate, and Whoop data from SQLite and summarize health metrics with coaching-style, non-medical guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajde0606](https://clawhub.ai/user/ajde0606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to answer Apple Health, live heart-rate, and Whoop questions from a trusted local SQLite database. It returns metric summaries, trends, alerts, workout and recovery context, and practical next steps with non-medical safety framing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health data from a local database.

Mitigation: Use it only with a trusted local database and review outputs before acting on health-related guidance.

Risk: Live-heart-rate queries may be weakly scoped in shared or multi-user tables.

Mitigation: Do not run live-heart-rate queries against shared tables unless a user-level filter is added.

Risk: Broad .env loading may expose unrelated secrets to the query scripts' process environment.

Mitigation: Keep unrelated secrets out of the same .env file used by this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajde0606/skills/apple-health-skills)
- [WHOOP Developer Platform](https://developer.whoop.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and summaries derived from JSON query output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite the queried time window, use observed values and timestamps, and state that health guidance is informational and not medical advice.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
