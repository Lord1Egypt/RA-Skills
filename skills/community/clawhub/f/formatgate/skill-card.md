## Description:

Convert between JSON, YAML, and TOML formats in all six directions for agents that receive data in one format and need it in another.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Formatgate to convert structured content among JSON, YAML, and TOML through a local API when a workflow needs a different data or configuration format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local conversion API may receive sensitive configuration or data.

Mitigation: Run it only in a controlled environment and avoid sending secrets unless you control the server.

Risk: Round-trip preservation is not guaranteed for every JSON, YAML, and TOML edge case.

Mitigation: Review converted output before using it in production configuration or automation.

Risk: The skill runs a local FastAPI service and downloads Python dependencies.

Mitigation: Install dependencies in an isolated environment and review dependency policy before deployment.

## Reference(s):

- [Formatgate on ClawHub](https://clawhub.ai/mirni/skills/formatgate)
- [Publisher profile: mirni](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration]

**Output Format:** [JSON API response containing converted JSON, YAML, or TOML text plus success or error fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input content is limited to 500,000 characters by the request model.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
