## Description:

Make paid requests to x402-enabled APIs using USDC on Base when the user explicitly asks to call a paid API, make an x402 payment, pay for a request, or fetch from a paid endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect x402 payment requirements, verify wallet balance, and make explicit paid API requests with USDC on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend USDC and send request URLs, bodies, headers, and responses to external services.

Mitigation: Require an explicit destination URL, payment network, maximum amount, and payload review before use.

Risk: The skill uses the mutable npx agnic@latest command, so the downloaded CLI can change between runs.

Mitigation: Pin the package version and control the execution environment for production or repeatable use.

Risk: Passing credentials with --token can expose secrets in process history or logs.

Mitigation: Prefer environment-based credentials such as AGNIC_TOKEN and avoid echoing or logging secrets.

## Reference(s):

- [x402 Protocol Reference](reference/x402-protocol.md)
- [ClawHub Skill Page](https://clawhub.ai/agnicpay-prog/skills/agnicpay-pay-for-service)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash commands and JSON output when --json is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external x402 services and return paid API responses.]

## Skill Version(s):

2.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
