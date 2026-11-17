## Description:

Get overview and status information from Clarity Protocol, including API info, variant counts, and endpoint availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarityprotocol](https://clawhub.ai/user/clarityprotocol)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and integrators use this skill to check Clarity Protocol API availability, understand available protein-folding research data, inspect endpoint coverage, and plan API integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts clarityprotocol.io and may send CLARITY_API_KEY if the user sets that environment variable.

Mitigation: Use the skill only when the Clarity Protocol service is trusted, and set CLARITY_API_KEY only when the higher authenticated rate limit is needed.

Risk: Live status output depends on Clarity Protocol API availability and rate limits.

Mitigation: Treat results as current API responses, retry after the service-provided delay when rate limited, and avoid relying on the output as an offline snapshot.

## Reference(s):

- [Clarity Protocol](https://clarityprotocol.io)
- [Clarity Protocol API v1](https://clarityprotocol.io/api/v1)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The status script emits either a human-readable summary or JSON containing API information and a variant count.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
