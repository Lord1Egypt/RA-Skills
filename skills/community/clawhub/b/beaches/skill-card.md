## Description:

Finds nearby beaches when a user asks for beaches near them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list beaches near a user-provided location with radius, limit, and optional filters for travel discovery and route planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Beach lookup requires user location data, which can expose precise coordinates if retained or reused unnecessarily.

Mitigation: Request location permission before lookup and avoid retaining exact coordinates beyond what is needed for the search.

Risk: Repeated location-based searches may increase privacy exposure or trigger provider rate limits.

Mitigation: Use short-term caching for location, category, and radius combinations and apply rate limiting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/beaches)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown or structured POI response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses location, radius, result limit, and optional filters such as open_now, min_rating, and keywords.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
