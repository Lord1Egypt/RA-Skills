## Description:

Plan Bulgaria with local context on Sofia, Plovdiv, the Black Sea, mountain routes, food, and tourist-trap avoidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan Bulgaria trips with practical local context across cities, coast, mountains, food, transport, lodging, family travel, and safety. It helps tailor recommendations by season and travel style while flagging tourist traps and logistical friction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store personal trip details and preferences in ~/bulgaria/.

Mitigation: Store only details that improve future recommendations, avoid sensitive exact itinerary or booking information unless needed, and review local memory notes periodically.

Risk: Proactive activation may surface travel advice when Bulgaria is mentioned even if the user only wanted one-off help.

Mitigation: Choose the non-proactive activation preference during setup if assistance should happen only when explicitly requested.

Risk: Travel advice about prices, schedules, openings, weather, and transport can become stale.

Mitigation: Check current details before booking, traveling, or committing to time-sensitive plans.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/bulgaria)
- [Skill Homepage](https://clawic.com/skills/bulgaria)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown travel-planning guidance and local memory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local trip notes under ~/bulgaria/ when memory setup is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
