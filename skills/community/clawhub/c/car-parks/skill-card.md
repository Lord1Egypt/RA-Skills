## Description:

Find nearby car parks when a user asks for parking near them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill to find nearby parking facilities from an authorized location, with optional radius, result limit, and availability or price filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses precise user location input to search for nearby parking.

Mitigation: Require explicit location authorization and avoid retaining exact coordinates beyond the task; use coordinate obfuscation when precision is unnecessary.

Risk: Parking results may be incomplete or temporarily unavailable because the skill depends on external provider data.

Mitigation: Surface provider failures with the documented PROVIDER_UNAVAILABLE or RATE_LIMITED error codes and avoid presenting unavailable data as confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeclaw007/skills/car-parks)
- [Publisher profile](https://clawhub.ai/user/mikeclaw007)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown guidance describing standardized parking search inputs, outputs, and errors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected outputs are standardized parking or POI lists with clear error codes for invalid locations, excessive radius, provider unavailability, and rate limiting.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
