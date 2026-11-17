## Description:

Find nearby bakeries. Invoke when user asks for bakeries near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find nearby bakeries from an authorized location or city request, with optional filters such as open-now status, rating, price level, and keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finding nearby bakeries may require sharing a user's current location with a place-search provider.

Mitigation: Request location only with user authorization, avoid retaining precise coordinates, and use coordinate fuzzing or short-term caching when appropriate.

Risk: Place-search providers can be unavailable or rate limited.

Mitigation: Surface provider and rate-limit errors clearly using the documented PROVIDER_UNAVAILABLE and RATE_LIMITED responses.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance describing location-based bakery search inputs, outputs, filters, error codes, privacy expectations, and rate-limit handling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a standard point-of-interest list for the fixed bakeries category; no executable code is included in the artifact.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
