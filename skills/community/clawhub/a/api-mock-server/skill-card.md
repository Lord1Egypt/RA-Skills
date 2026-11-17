## Description:

Lightweight API mock server for prototyping and testing, supporting JSON and JSON Schema responses, dynamic data, validation, latency, and webhook simulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to create local mock HTTP APIs for frontend-backend decoupling, automated tests, prototyping, request validation, latency simulation, and webhook testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The mock server can expose unauthenticated routes on all network interfaces by default.

Mitigation: Bind to 127.0.0.1 unless remote access is intentionally required, avoid sensitive test data in mock routes, and use firewall controls on shared networks.

Risk: Runtime dependencies are specified as open version ranges.

Mitigation: Review and pin dependencies before use in controlled or production-like environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/api-mock-server)
- [Publisher profile](https://clawhub.ai/user/kaiyuelv)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include route definitions, JSON configuration examples, dependency installation commands, and local server startup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
