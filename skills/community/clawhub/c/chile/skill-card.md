## Description: <br>
Plan Chile trips with macro-region triage, verified entry rules, long-distance logistics, and practical safety for cities, desert, lakes, and Patagonia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to plan Chile trips, choose realistic macro-regions, compare faster and slower logistics models, and account for entry, SAG declaration, weather, safety, reservation, and budget constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local trip memory may include dates, budget, mobility, dietary preferences, itinerary constraints, and other personal travel context. <br>
Mitigation: Review or delete ~/chile/memory.md when those details should not be reused, and avoid storing unnecessary sensitive details. <br>
Risk: Entry, biosecurity, park, transport, and emergency guidance can become stale before a trip. <br>
Mitigation: Refresh official sources from sources.md before non-refundable bookings, border decisions, park visits, or safety-sensitive travel. <br>
Risk: Chile travel plans can be disrupted by altitude, Patagonia weather, closures, strikes, ferries, or long transfer chains. <br>
Mitigation: Keep backup routing, verify local alerts and operator updates, and include margin before high-altitude days, long drives, ferries, and major treks. <br>


## Reference(s): <br>
- [Chile ClawHub release page](https://clawhub.ai/ivangdavila/chile) <br>
- [Chile skill homepage](https://clawic.com/skills/chile) <br>
- [Official source map](artifact/sources.md) <br>
- [Chile Travel entry and visa requirements](https://stg.chile.travel/en/good-to-know/entry-and-visa-requirements/) <br>
- [SAG traveler declaration](https://www.sag.gob.cl/ambitos-de-accion/declaracion-jurada-del-sag-para-viajeros) <br>
- [Pases Parques official portal](https://www.pasesparques.cl/es) <br>
- [SENAPRED](https://www.senapred.cl/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prose, checklists, itinerary outlines, logistics comparisons, and occasional shell commands for local setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain trip context in ~/chile/memory.md when the user enables or continues local memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
