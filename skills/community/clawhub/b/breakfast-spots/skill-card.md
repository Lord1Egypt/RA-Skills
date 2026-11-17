## Description:

Find nearby breakfast spots when a user asks for breakfast near them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request user-authorized nearby breakfast, brunch, coffee, and bakery spot recommendations from a supplied location or city.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise location or city data can expose sensitive personal context if collected without consent or retained longer than necessary.

Mitigation: Request user authorization before querying, avoid retaining precise coordinates, and obfuscate coordinates or use short-term caching only when needed.

Risk: Provider outages or rate limits can prevent complete nearby-place results.

Mitigation: Surface provider and rate-limit errors clearly instead of presenting unavailable data as current or complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawkk/skills/breakfast-spots)
- [ClawHub publisher profile](https://clawhub.ai/user/clawkk)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured POI list with category breakfast-spots and optional explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-authorized location or city input; supports radius, limit, and optional filters.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
