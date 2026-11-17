## Description:

Find nearby brunch spots. Invoke when user asks for brunch near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill to find brunch spots near a current location or specified city with filters such as radius, rating, price level, and open-now status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses current location to find nearby brunch spots, which can expose precise coordinates if provider queries or caching are handled without privacy controls.

Mitigation: Request location only after user authorization, avoid retaining exact coordinates, use grid-based obfuscation where practical, and keep location-area caching short-lived.

Risk: Place data providers can be unavailable or rate-limited, leading to incomplete or failed brunch recommendations.

Mitigation: Surface explicit provider-unavailable and rate-limited errors, keep query radius within configured limits, and use short-term caching for repeated searches in the same area.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawkk/skills/brunch-spots)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown or structured place-list response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a standardized point-of-interest list for the brunch-spots category.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
