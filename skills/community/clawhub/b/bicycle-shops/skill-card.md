## Description:

Find nearby bicycle shops. Invoke when user asks for bike shops near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to find nearby bicycle shops for purchases, accessories, repairs, or maintenance based on an authorized location, radius, and optional filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nearby shop searches may expose a user's precise location.

Mitigation: Query only after user authorization, prefer approximate or grid-obscured coordinates where possible, and avoid retaining precise coordinates.

Risk: The referenced STANDARD_RESPONSE.md schema is not included in the package, which can create response-format ambiguity for integrators.

Mitigation: Confirm the expected POI response schema in the consuming system before deployment.

Risk: Provider outages or rate limits may prevent successful lookup results.

Mitigation: Handle PROVIDER_UNAVAILABLE and RATE_LIMITED responses and use short-term caching for repeated location, category, and radius requests.

## Reference(s):

- [Nearby Bicycle Shops on ClawHub](https://clawhub.ai/codekungfu/skills/bicycle-shops)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Standardized POI list with location-aware shop results, filters, and error codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorized location; category is fixed to bicycle-shops; default radius is 3000 meters; default limit is 20 and maximum limit is 50.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
