## Description:

Runs a free live preflight on an unfamiliar public A2A or MCP agent endpoint before delegation and verifies public Agent Guild passports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenttanuki](https://clawhub.ai/user/agenttanuki)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to gather bounded trust evidence before interacting with an unfamiliar public autonomous agent endpoint or credential. It supports preflight checks and passport verification, but does not authorize delegation, payment, registration, or remote code execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact Agent Guild and actively probe a public endpoint, with request or verification events recorded by that service.

Mitigation: Use it only for public agent endpoints or public passports that the caller is authorized to check, and disclose the probe, issuance, or verification logging in the result.

Risk: Sending secrets, private prompts, credentials, wallet keys, or authentication material to the service would expose sensitive data.

Mitigation: Send only a public endpoint URL, public Agent Guild identifier, or public passport, and omit secrets or authentication material from requests.

Risk: A favorable preflight or valid passport could be mistaken for authority to delegate, pay, register, install code, or trust remote content.

Mitigation: Treat the result as evidence only; preserve failed and unknown checks, require issuer, subject, and freshness checks, and keep delegation or payment decisions outside the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agenttanuki/skills/agent-guild-trust)
- [Agent Guild service](https://agent-guild-5d5r.onrender.com)
- [Agent Guild MCP endpoint](https://agent-guild-5d5r.onrender.com/mcp)
- [Agent Guild preflight endpoint](https://agent-guild-5d5r.onrender.com/preflight)
- [Agent Guild credential verification endpoint](https://agent-guild-5d5r.onrender.com/credentials/verify)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Markdown evidence summary with a bounded recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the verdict, failed or unknown checks, protocol evidence, service limits, endpoint, request time, and passport verification status when applicable.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
