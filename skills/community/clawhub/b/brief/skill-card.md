## Description:

Turns raw material into decision-ready briefs such as executive summaries, status updates, meeting pre-reads, and decision documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and teams use Brief to turn user-provided reports, threads, transcripts, or project material into action-oriented briefs for decisions, meetings, incidents, handoffs, and recurring status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local formatting preferences under ~/Clawic/data/brief/ can change how future briefs are structured.

Mitigation: Review config.yaml and preferences.md when brief style changes unexpectedly, and update or remove stale preferences.

Risk: Older preference folders may contain outdated or unintended settings if migrated blindly.

Mitigation: Confirm any migration from ~/brief/ or ~/clawic/brief/ before moving data into ~/Clawic/data/brief/.

Risk: Briefs can mislead readers when source material is stale, conflicting, or missing a decision context.

Mitigation: Use the skill's source gates: require user-provided or user-specified sources, show conflicts with provenance, include as-of dates for stale data, and ask what decision the brief should support when unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/brief)
- [Clawic Brief skill page](https://clawic.com/skills/brief)
- [Brief skill definition](artifact/SKILL.md)
- [Brief templates](artifact/templates.md)
- [Source handling guidance](artifact/sources.md)
- [First-use setup](artifact/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text brief structures with bullets, status labels, asks, source lines, and optional local preference files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local formatting preferences in ~/Clawic/data/brief/ and use ~/Clawic/profile.yaml for locale/timezone fallback.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
