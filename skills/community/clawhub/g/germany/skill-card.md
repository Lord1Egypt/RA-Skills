## Description:

Plan Germany trips with region-specific routing, rail-vs-car strategy, verified entry rules, and practical travel logistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and trip-planning agents use this skill to build practical Germany itineraries, choose regions, compare rail and car logistics, check Schengen and border planning needs, and account for seasons, budget, payments, safety, and accessibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist trip preferences and constraints in ~/germany/memory.md.

Mitigation: Avoid storing sensitive travel details, review the local memory file as needed, and delete ~/germany/memory.md or ~/germany/ to clear saved context.

Risk: Entry, EES, ETIAS, customs, weather, transport, and event details can change after the skill's sources were last checked.

Mitigation: Re-check the official references in artifact/sources.md before making non-refundable bookings or giving final entry, border, safety, or disruption-sensitive advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/germany)
- [Skill homepage](https://clawic.com/skills/germany)
- [Sources - Germany Skill](artifact/sources.md)
- [German Federal Foreign Office](https://www.auswaertiges-amt.de/en)
- [Your Europe travel and entry rights](https://europa.eu/youreurope/citizens/travel/index_en.htm)
- [ETIAS official portal](https://travel-europe.europa.eu/etias_en)
- [Entry Exit System official portal](https://travel-europe.europa.eu/ees_en)
- [German Customs](https://www.zoll.de/EN/Home/home_node.html)
- [Deutsche Bahn international portal](https://int.bahn.de/en)
- [German Weather Service](https://www.dwd.de/EN/Home/home_node.html)
- [Germany Travel official tourism portal](https://www.germany.travel/en/home.html)
- [Barrier-free travel in Germany](https://www.germany.travel/en/barrier-free-travel/barrier-free-travel.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel guidance with optional inline bash setup commands and local memory updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local trip context in ~/germany/memory.md.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
