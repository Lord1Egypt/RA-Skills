## Description:

Find nearby bars. Invoke when user asks for drinks or nightlife near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to find nearby bars or nightlife options from an authorized location, with optional filters such as open-now status, rating, price level, and keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise location can reveal sensitive user whereabouts.

Mitigation: Use the skill only after location permission, avoid retaining exact coordinates, and prefer coarse or short-lived cached location data when caching is needed.

Risk: Ambiguous nightlife requests may not always mean bars.

Mitigation: Clarify ambiguous requests before searching when the user may want a different venue category.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Text, JSON]

**Output Format:** [Structured POI results using a standard response schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include location, radius, limit, category, filters, venue details, and error codes.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
