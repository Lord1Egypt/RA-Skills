## Description:

Find nearby barbershops. Invoke when user asks for a haircut near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find barbershops near an authorized location and return a standardized point-of-interest list with filters such as open status, rating, price level, and keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses precise location data to find nearby barbershops.

Mitigation: Use location only after user authorization, avoid retaining precise coordinates, and apply grid-based fuzzing when exact coordinates are not required.

Risk: Place lookup results may fail or be throttled by an upstream data source.

Mitigation: Surface standard errors such as PROVIDER_UNAVAILABLE and RATE_LIMITED, and use short-term caching for repeated nearby queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawkk/skills/barbershops)
- [Publisher profile](https://clawhub.ai/user/clawkk)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON-compatible structured point-of-interest list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include standard location, category, radius, result limit, filter, and error-code fields.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
