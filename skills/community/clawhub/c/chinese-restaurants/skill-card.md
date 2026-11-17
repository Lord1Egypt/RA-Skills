## Description:

Find nearby Chinese restaurants when users ask for Chinese food near them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for nearby Chinese restaurant options based on an authorized location, radius, limit, and optional filters such as open now, rating, price level, or keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise user location could be exposed or retained longer than needed during restaurant search.

Mitigation: Request location permission, use location only for the stated restaurant search, avoid retaining precise coordinates, and limit any caching to short-term location-category-radius data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Structured POI list with standardized fields and error codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-authorized location input; supports radius, result limit, and optional restaurant filters.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
