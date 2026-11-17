## Description:

Get detailed routing between two points with distance, duration, and optional turn-by-turn directions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request route distance, travel duration, and optional turn-by-turn directions between coordinate pairs for driving, cycling, or walking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends route coordinates and optional imagery requests to Camino's API under the user's API key.

Mitigation: Do not submit home, work, live, or otherwise sensitive locations unless you are comfortable sharing those coordinates and optional imagery requests with Camino.

Risk: Install instructions include mutable package or repository targets and an all-skills install option.

Mitigation: Install only from a reviewed, pinned source when possible, and avoid the all-skills install unless you intend to trust the entire Camino suite.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/skills/camino-route)
- [Camino API key activation](https://app.getcamino.ai/skills/activate)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON route data and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAMINO_API_KEY plus curl and jq; optional geometry and imagery parameters may increase location-data sensitivity.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
