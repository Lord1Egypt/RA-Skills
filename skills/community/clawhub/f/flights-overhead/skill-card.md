## Description:

See what flights are above you right now. Identify contrails, planes overhead, and nearby air traffic using OpenSky Network (free, no key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[sundiraman](https://clawhub.ai/user/sundiraman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to identify flights currently overhead or nearby, including contrails and visible aircraft. The skill guides the agent to obtain a confirmed location, query nearby air traffic, and present concise flight details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location privacy exposure when coordinates or a saved home address are used for third-party flight lookup.

Mitigation: Use only a location the user intentionally provides or confirms, and prefer coarse city or neighborhood-level location when that is sufficient.

Risk: The referenced flight script was not included in the reviewed artifact.

Mitigation: Verify the required flight lookup script is present and reviewed before relying on this skill for execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Markdown]

**Output Format:** [Markdown guidance with bash examples and a JSON flight-result structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a confirmed or intentionally provided latitude and longitude, plus optional radius, limit, and JSON-output parameters.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
