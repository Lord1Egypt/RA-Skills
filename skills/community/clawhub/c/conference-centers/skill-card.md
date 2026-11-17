## Description:

Find nearby conference centers. Invoke when user asks for conference venues near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find nearby conference centers, event venues, and meeting spaces from an authorized location with optional rating, price, and keyword filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses precise latitude and longitude, which can expose sensitive location information if retained or shared unnecessarily.

Mitigation: Request location authorization, use coordinates only when needed for venue lookup, and avoid storing precise coordinates longer than necessary.

Risk: Venue lookup may fail or degrade when the location provider is unavailable, rate-limited, or queried with invalid bounds.

Mitigation: Validate location, radius, and result limits before lookup, then return clear error states for invalid input, provider outages, and rate limiting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/conference-centers)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured text or JSON-like POI list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorized latitude and longitude; supports radius, result limit, rating, price, and keyword filters.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
