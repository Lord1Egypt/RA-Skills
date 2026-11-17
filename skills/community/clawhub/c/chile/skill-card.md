## Description:

Plan Chile trips with macro-region triage, verified entry rules, long-distance logistics, and practical safety for cities, desert, lakes, and Patagonia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan Chile travel with region selection, routing, entry and biosecurity checks, weather-aware logistics, safety notes, and booking priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist Chile trip details in ~/chile/memory.md for reuse across sessions.

Mitigation: Avoid storing sensitive personal details in the local memory file, and delete ~/chile/memory.md when the user wants to clear stored trip context.

Risk: Travel rules, park access, weather disruptions, and transport details can change after the skill's source checks.

Mitigation: Verify time-sensitive entry, SAG, Rapa Nui, park, weather, and transport details against the official source map before booking or travel.

## Reference(s):

- [Chile ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/chile)
- [Chile Skill Homepage](https://clawic.com/skills/chile)
- [Official Source Map](artifact/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel-planning guidance with optional shell commands for local trip memory setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local trip memory under ~/chile/ when the user uses the setup workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
