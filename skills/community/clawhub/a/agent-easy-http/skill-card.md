## Description:

Deploy an HTTP(S) proxy that exposes OpenClaw agent capabilities as a REST API over a network IP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

Developers and platform operators use the skill to deploy an internal HTTP(S) API for invoking OpenClaw agents or selected skills and retrieving their results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service exposes a remotely callable agent interface.

Mitigation: Limit access to trusted callers, keep API-key authentication enabled, and leave /agent/run disabled unless required.

Risk: Plain HTTP can expose credentials, prompts, and results in transit.

Mitigation: Use HTTPS for cross-host access or restrict HTTP to localhost or a trusted network.

Risk: Setup can make persistent service and configuration changes; the security guidance also notes possible root execution.

Mitigation: Review hook and service changes, and run the service with only the permissions it needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/agent-easy-http)
- [Deployment guide](references/deployment.md)
- [TLS and authentication standard](references/tls-auth-standard.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions]

**Output Format:** [REST API request and response JSON with Markdown setup guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent results are retrieved asynchronously by run ID.]

## Skill Version(s):

1.1.0 (source: CHANGELOG.md, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
