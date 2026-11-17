## Description:

Find nearby budget hotels. Invoke when user asks for cheap hotels near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find nearby budget hotels or temporary low-cost accommodations from a user-authorized location, with optional filters such as radius, result limit, price level, rating, breakfast, and keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use precise location data to search for nearby hotels.

Mitigation: Only request precise coordinates when the user intends to search, and avoid retaining exact coordinates unnecessarily.

Risk: Hotel provider unavailability or rate limiting can prevent complete results.

Mitigation: Return clear provider-unavailable or rate-limited errors and use short-lived caching where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawkk/skills/budget-hotels)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Text]

**Output Format:** [Markdown guidance describing inputs, response fields, error codes, and privacy considerations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces standardized nearby hotel lookup guidance; no executable code is included in the artifact.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
