## Description:

Plan Finland trips with verified entry rules, season-aware routing, rail-and-Lapland logistics, and practical tourist safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to build operational Finland itineraries with Schengen entry checks, season-aware route choices, transport tradeoffs, budget realism, and practical safety notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local trip memory under ~/finland/ may contain travel preferences, itinerary details, budget, mobility needs, or other personal context.

Mitigation: Avoid storing highly sensitive details unless needed, and review or delete ~/finland/memory.md when the trip is over.

Risk: Entry rules, EES/ETIAS rollout details, border restrictions, weather warnings, and transport schedules can change after the skill content was last checked.

Mitigation: Verify current requirements and conditions with the official sources listed in sources.md before booking non-refundable travel or departing.

Risk: Winter, Lapland, archipelago, and remote nature plans can be affected by cold, darkness, road conditions, ferry frequency, and emergency-access constraints.

Mitigation: Keep routes season-specific, include transfer buffers and fallback plans, and check official weather, road, ferry, and emergency guidance before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/finland)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Skill homepage](https://clawic.com/skills/finland)
- [Official source map](sources.md)
- [Finland Abroad visitor visa guidance](https://finlandabroad.fi/web/eng/visa-to-visit-finland)
- [Finnish Immigration Service](https://migri.fi/en/coming-to-finland)
- [EU travel to Europe portal](https://travel-europe.europa.eu/)
- [Finnish Border Guard](https://raja.fi/en/frontpage)
- [Finnish Customs traveller guidance](https://tulli.fi/en/private-persons/travelling)
- [HSL Helsinki region transport](https://www.hsl.fi/en)
- [VR trains and night trains](https://www.vr.fi/en)
- [Finnish Meteorological Institute](https://en.ilmatieteenlaitos.fi/)
- [112 Suomi emergency guidance](https://112.fi/en)
- [Visit Finland](https://www.visitfinland.com/en/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with occasional shell commands and local trip-memory updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local trip context under ~/finland/ when available; does not make network requests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
