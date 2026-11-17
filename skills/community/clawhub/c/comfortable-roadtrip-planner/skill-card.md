## Description:

Plans comfort-first multi-day self-drive trips and can produce a one-file interactive HTML route app with maps, prioritized stops, weather, meals, rest breaks, tickets, map-provider links, and calendar import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crazyricemaker](https://clawhub.ai/user/crazyricemaker)

### License/Terms of Use:

MIT

## Use Case:

External travelers and trip-planning agents use this skill to turn fixed hotels, dates, route constraints, and stamina needs into a comfortable self-drive itinerary with skippable A/B/C stops and an optional interactive route artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented HTML validation workflow can execute JavaScript from the route artifact being checked.

Mitigation: Run validation and evaluation scripts only on HTML artifacts you created or otherwise trust; do not run them on untrusted injected trip data.

Risk: Generated trip artifacts can expose private home addresses, hotel confirmations, medical details, or personal constraints if shared publicly.

Mitigation: Redact private traveler and booking details from shared artifacts, and keep sensitive itinerary versions local unless the user explicitly requests sharing.

Risk: Map-provider links can disclose route and stop data to the selected map provider.

Mitigation: Tell users that opening Apple, Google, Amap, or Baidu map links shares route data with those providers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/crazyricemaker/skills/comfortable-roadtrip-planner)
- [Project Homepage](https://github.com/CrazyRiceMaker/comfortable-roadtrip-planner)
- [Public Landing Page](https://crazyricemaker.github.io/comfortable-roadtrip-planner/)
- [Comfort Routing Reference](references/comfort-routing.md)
- [Artifact Patterns](references/artifact-patterns.md)
- [Interactive HTML Route App Reference](references/interactive-html-artifact.md)
- [Trip Data Contract](references/trip-data-contract.md)
- [Trip Data Schema](schemas/trip-data.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, one-file HTML route app code, structured trip data, calendar import content, and validation commands when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include source provenance for volatile travel facts and should avoid exposing private addresses, booking confirmations, medical details, or personal constraints in public artifacts.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
