## Description:

Find nearby bookshops when the user asks for bookstores near them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and application agents use this skill to find nearby bookshops, second-hand book stores, and reading spaces from an authorized location or city.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses precise or user-authorized location data to find nearby bookshops.

Mitigation: Request location only after user authorization, avoid retaining precise coordinates, and use grid-based obfuscation when exact coordinates are not required.

Risk: Repeated nearby searches may increase provider rate-limit exposure or unnecessary location processing.

Mitigation: Use short-lived caching for the same location, category, and radius, and handle provider unavailable or rate-limited responses explicitly.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with standardized POI response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should follow a standardized point-of-interest list for the bookshops category.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
