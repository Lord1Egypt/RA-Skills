## Description:

Plan Colombia trips with region-specific routing, verified entry rules, weather-aware logistics, and practical tourist safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to design Colombia itineraries, compare regions, handle entry and health checks, and plan realistic transport, weather, budget, safety, and booking logistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip details may be retained locally in ~/colombia/memory.md, including sensitive health or identity context if the user adds it.

Mitigation: Avoid storing sensitive health or identity details unless they are necessary for the trip, and edit or delete the local memory file when retained context is no longer wanted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/colombia)
- [Skill homepage](https://clawic.com/skills/colombia)
- [Colombia skill sources](sources.md)
- [Cancilleria visa requirements](https://www.cancilleria.gov.co/tramites_servicios/visa/requisitos)
- [Migracion Colombia Check-Mig](https://apps.migracioncolombia.gov.co/pre-registro/en/)
- [Colombia Travel practical information](https://colombia.travel/en/practical-information)
- [Minsalud yellow fever guidance](https://www.minsalud.gov.co/salud/publica/PET/Paginas/fiebre-amarilla.aspx)
- [IDEAM forecasts and alerts](https://www.ideam.gov.co/pronosticos-y-alertas)
- [INVIAS road information system](https://hermes2.invias.gov.co/SIV/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown travel-planning guidance with checklists, route models, and day-by-day itinerary structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local trip preferences stored in ~/colombia/memory.md when available]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
