## Description:

Ctrip helps agents retrieve and summarize public Ctrip hotel, flight, and itinerary pages for lightweight travel analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to summarize public Ctrip hotel and flight pages, compare prices and schedules, and assemble lightweight itinerary lists without booking or authenticated account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill for account actions, bookings, authenticated pages, bulk scraping, or attempts to bypass Ctrip protections could violate platform rules.

Mitigation: Limit use to public pages, lightweight summaries, and manually initiated parsing; do not automate account actions, bookings, or security bypasses.

Risk: Travel prices and inventory can change after collection.

Mitigation: Report collection time and treat prices and availability as point-in-time observations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/ctrip-hot-trend)
- [Ctrip](https://www.ctrip.com/)
- [Ctrip Hotels](https://hotels.ctrip.com/)
- [Ctrip Flights](https://flights.ctrip.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise text summaries of travel listings, comparisons, and itinerary notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Should include collection time for volatile prices and inventory when reporting extracted travel data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
