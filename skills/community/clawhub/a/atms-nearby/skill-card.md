## Description:

Find nearby ATMs. Invoke when user asks for cash withdrawal near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill after sharing location to find nearby ATMs for cash withdrawal and receive standardized POI-style results for frontend or API reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise location may reveal sensitive user movement or banking intent.

Mitigation: Invoke only after the user chooses to share location, and avoid retaining precise coordinates; use grid-level blurring when storage or logging is necessary.

Risk: Broad banking-related wording could trigger the skill for general banking questions instead of nearby ATM lookup.

Mitigation: Limit activation to nearby ATM or cash-withdrawal intent that includes or requests a location.

Risk: Invalid coordinates, excessive radius, provider outages, or rate limits may produce incomplete results.

Mitigation: Validate latitude, longitude, radius, and limit before lookup, and surface the documented error states when providers are unavailable or rate limited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeclaw007/skills/atms-nearby)
- [Publisher profile](https://clawhub.ai/user/mikeclaw007)

## Skill Output:

**Output Type(s):** [guidance, text, JSON]

**Output Format:** [Text guidance with structured JSON-style POI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Location is required; radius defaults to 3000 meters; limit defaults to 20 and maxes at 50; optional ATM filters may apply.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
