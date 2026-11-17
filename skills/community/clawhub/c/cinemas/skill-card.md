## Description:

Find nearby cinemas. Invoke when user asks for movie theaters near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find nearby movie theaters from an authorized location, with optional radius, limit, IMAX, rating, and open-status filters. It also defines consistent point-of-interest response behavior, category labeling, error handling, and privacy expectations for location data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact refers to an absolute local STANDARD_RESPONSE.md file that is not packaged with the skill, so users cannot independently review the complete response format from this release alone.

Mitigation: Ask the publisher to package the response-format reference as a relative file or remove the external local reference before deployment.

Risk: The skill handles precise user location coordinates, which can create privacy risk if queried or retained without clear authorization.

Mitigation: Require user authorization before location lookup and blur or grid coordinates when exact precision is not necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeclaw007/skills/cinemas)

## Skill Output:

**Output Type(s):** [Guidance, Text, Configuration]

**Output Format:** [Markdown guidance with JSON-like input and output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes required location input, search radius and limit settings, optional filters, standardized cinema category output, error codes, and privacy constraints.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
