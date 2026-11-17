## Description:

Find nearby bubble tea shops. Invoke when user asks for boba near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to answer nearby boba or bubble tea searches from an authorized location or city, returning a consistent point-of-interest list with optional filters for open status, rating, price, and keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nearby search requires sharing a user location with the host app or its location provider.

Mitigation: Request user authorization before querying and avoid retaining precise coordinates; confirm the host app follows the stated privacy expectation.

Risk: Invalid locations, excessive radius, provider outages, or rate limits can prevent a complete nearby-shop response.

Mitigation: Validate coordinates, enforce radius and result limits, and surface clear errors such as INVALID_LOCATION, RADIUS_TOO_LARGE, PROVIDER_UNAVAILABLE, and RATE_LIMITED.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Standardized point-of-interest list or concise natural-language response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authorized location, optional radius and limit bounds, and optional filters such as open_now, min_rating, price_level, and keywords.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
