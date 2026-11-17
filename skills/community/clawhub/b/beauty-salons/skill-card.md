## Description:

Find nearby beauty salons. Invoke when user asks for beauty services near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find nearby beauty salons from an authorized location, with common filters such as open status, rating, price level, and keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses location data to find nearby salons, which can expose sensitive personal context if over-collected or retained.

Mitigation: Use the skill only after the user intentionally requests nearby beauty services and authorizes location use; avoid retaining precise coordinates and coarsen them when possible.

Risk: Nearby salon results can be incomplete, stale, unavailable, or rate limited by the provider.

Mitigation: Surface provider, radius, location, and rate-limit errors clearly instead of presenting unavailable results as authoritative.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown or JSON-like POI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns standardized point-of-interest fields and related error states for invalid location, excessive radius, provider unavailability, and rate limiting.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
