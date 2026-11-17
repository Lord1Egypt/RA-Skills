## Description:

Amap Date Spot helps an agent recommend date or meetup venues using Amap POI, routing, weather, and venue signals, then produces three options with rationale, an itinerary, photo tips, parking details, and backup choices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongdongyue](https://clawhub.ai/user/dongdongyue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to choose date, meetup, friendship, or business-chat locations from one place or a midpoint between two locations. It guides venue selection, route planning, timing, weather-aware adjustments, parking notes, and alternatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive meeting areas, route details, and relationship context.

Mitigation: Use coarse meeting areas unless exact routing is necessary, and do not enter another person's precise location without permission.

Risk: Recommended plans may contain addresses, routes, and meeting details that become sensitive if exported or shared.

Mitigation: Review outputs before sharing and avoid generating shareable CSV or HTML artifacts unless those details are intended for that audience.

## Reference(s):

- [Server-resolved source repository](https://github.com/dongdongyue/amap-date-spot)
- [ClawHub skill page](https://clawhub.ai/dongdongyue/skills/amap-date-spot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style recommendations with venue summaries, itinerary steps, travel notes, photo suggestions, parking information, and alternatives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AMAP_API_KEY for Amap-backed place, route, detail, and weather lookups when available.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; source skill frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
