## Description:

Plan Austria trips with rail and road logic, alpine season timing, region-specific routing, and practical local execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to plan Austria itineraries that account for entry rules, regional routing, rail-versus-car choices, alpine seasonality, budgets, safety, and practical execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip preferences are stored locally in ~/austria/memory.md and may be reused in later planning sessions.

Mitigation: Review or delete ~/austria/memory.md on shared devices or when stored trip context should no longer be retained.

Risk: Entry, customs, ETIAS, weather, transport, avalanche, and lift-status guidance can change before travel.

Mitigation: Verify current rules and operating conditions with official sources before booking non-refundable items, crossing borders, driving, hiking, or skiing.

## Reference(s):

- [ClawHub Austria skill page](https://clawhub.ai/ivangdavila/skills/austria)
- [Austria skill homepage](https://clawic.com/skills/austria)
- [Sources - Austria Skill](artifact/sources.md)
- [Austria government portal - entering and residing](https://www.oesterreich.gv.at/en/themen/leben_in_oesterreich/aufenthalt.html)
- [Austrian foreign ministry - visa information](https://www.bmeia.gv.at/en/travel-stay/entry-and-residence-in-austria/visa-information)
- [EU travel portal - ETIAS](https://travel-europe.europa.eu/etias_en)
- [OeBB travel planner and tickets](https://www.oebb.at/en/)
- [ASFINAG vignette and tolls](https://www.asfinag.at/en/toll/vignette/)
- [GeoSphere Austria weather portal](https://www.geosphere.at/)
- [Avalanche reports portal](https://lawinen.report/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with itinerary structures, checklists, decision frameworks, and occasional shell commands for local trip memory setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local trip preferences in ~/austria/memory.md; does not require binaries or network access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
