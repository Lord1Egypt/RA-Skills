## Description:

Formats JSON input into readable, indented output using Expanso Edge CLI or HTTP server pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to pretty-print compact JSON into a readable formatted string for inspection, logs, and tool output review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional HTTP server mode can create network exposure if bound beyond a trusted local environment.

Mitigation: Bind server usage to localhost or place it behind access controls, resource limits, and request-size limits before using it on shared or public networks.

Risk: Large JSON payloads can consume local processing resources.

Mitigation: Use request-size limits and resource limits appropriate to the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-json-pretty)
- [Publisher profile](https://clawhub.ai/user/aronchick)
- [Expanso](https://expanso.io)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object containing a formatted JSON string, validity flag, and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts JSON input as a string and supports an indentation parameter with a default of 2.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
