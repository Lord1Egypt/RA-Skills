## Description:

Find nearby auto repair services when a user asks for car repair near them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill to find nearby auto repair services from an authorized location, with optional radius, result limit, and service filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references a non-portable absolute STANDARD_RESPONSE.md path outside the reviewed skill package.

Mitigation: Confirm the publisher fixes or accepts the packaging issue before installation; do not rely on that external local path as reviewed content.

Risk: The skill requires user location input for nearby auto repair lookup.

Mitigation: Use it only after location authorization and avoid retaining precise coordinates; blur or grid coordinates when storage or forwarding is necessary.

Risk: Broad trigger wording may cause the skill to be invoked for general car repair questions.

Mitigation: Invoke it only when the user asks for nearby repair options or otherwise authorizes a location-based auto repair search.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeclaw007/skills/auto-repair)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Structured text describing nearby auto repair points of interest and related error codes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-authorized location; defaults to a 3000 meter radius and 20 results, with a maximum of 50 results.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
