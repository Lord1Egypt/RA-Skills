## Description:

Plan Denmark trips with compact route logic, verified entry rules, island transport choices, and practical local execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to build practical Denmark itineraries, choose regions and transport modes, check entry and customs friction, and account for seasonality, budget, accessibility, safety, and local logistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags unclear memory handling: the skill asks the agent to save a future activation preference in unspecified main memory while saying data stays under ~/denmark/.

Mitigation: Before use, confirm where trip details and activation preferences are stored, how to inspect or delete them, and avoid storing sensitive family, mobility, passport, or booking details unless needed.

Risk: Travel planning may depend on current entry rules, customs thresholds, transport schedules, ferry availability, weather warnings, and emergency guidance.

Mitigation: Verify time-sensitive trip decisions against the official sources listed in sources.md before booking or travel.

## Reference(s):

- [ClawHub Denmark Skill Page](https://clawhub.ai/ivangdavila/skills/denmark)
- [Denmark Skill Homepage](https://clawic.com/skills/denmark)
- [Official Source Map](sources.md)
- [New to Denmark Short-Stay Visa Guidance](https://nyidanmark.dk/en-GB/You-want-to-apply/Short-stay-visa)
- [Danish Customs Travel Rules](https://toldst.dk/en-us/individuals/travel)
- [DSB English Portal](https://www.dsb.dk/en/)
- [DMI Dangerous Weather Warnings](https://www.dmi.dk/varsler/varsler-om-farligt-vejr-i-danmark/)
- [VisitDenmark Planning Portal](https://www.visitdenmark.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown travel plans, checklists, routing guidance, and local memory setup notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain trip context in ~/denmark/memory.md and may ask about activation preferences for future Denmark planning.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
