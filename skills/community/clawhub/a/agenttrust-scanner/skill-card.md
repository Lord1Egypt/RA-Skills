## Description:

AgentTrust scans AI agent skills and MCP server manifests for security threats and returns signed ACT/HALT trust receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poteshniy](https://clawhub.ai/user/poteshniy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to assess SKILL.md files, MCP manifests, endpoint reputation, and wallet trust signals before an agent installs, trusts, or calls external tools. The skill is intended for workflows where users explicitly approve any outbound submission and redact sensitive content first.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill or manifest content may be transmitted outside the local machine to agenttrust.uk.

Mitigation: Ask for explicit approval before each submission and disclose that the selected content will leave the local environment.

Risk: Submitted content may contain credentials, tokens, internal URLs, or other sensitive material.

Mitigation: Redact secrets and internal details by default, skip submission when redaction is not sufficient, and prefer local summarization for sensitive material.

Risk: Paid endpoints may incur x402 USDC charges on Base.

Mitigation: Confirm the exact cost with the user before using any paid endpoint.

Risk: Installing the MCP server fetches an npm package.

Mitigation: Verify the pinned package version, publisher, and integrity before adding the MCP server configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/poteshniy/skills/agenttrust-scanner)
- [AgentTrust service host](https://agenttrust.uk)
- [AgentTrust JWKS](https://agenttrust.uk/.well-known/jwks.json)
- [IETF Verification State draft](https://datatracker.ietf.org/doc/draft-krausz-verification-state/)
- [AgentTrust receipt mapping](https://raw.githubusercontent.com/poteshniy/agenttrust/main/docs/mapping-v0.3.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with endpoint descriptions, shell commands, JSON configuration, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit per-request consent before transmitting content to agenttrust.uk; paid endpoints require explicit x402 USDC cost confirmation.]

## Skill Version(s):

1.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
