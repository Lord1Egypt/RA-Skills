## Description:

Provides AI agents with bounded funds on Base Mainnet to pay APIs and merchants, send human payouts, manage payment slips, and verify receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naraprotocol](https://clawhub.ai/user/naraprotocol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to give agents limited Base Mainnet funds for paying HTTP 402 APIs or merchants, sending payouts, and verifying receipts. It supports scoped spending without providing an agent a master wallet private key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review advises considering the npx reference before installing.

Mitigation: Use the documented pinned package version @cryptoslip/mcp@1.0.2 and review the package before running it.

Risk: Security checks were incomplete because six local path-like references in SKILL.md did not resolve to bundled files.

Mitigation: Review or confirm those referenced files separately before relying on claims that depend on them.

Risk: A publicly exposed claim link could let an unintended person claim its funds.

Mitigation: Send claim links only in a private message to the intended recipient, or use the documented code option.

## Reference(s):

- [Server-resolved source: NARAProtocol/cryptoslip-sdk, skills/cryptoslip](https://github.com/NARAProtocol/cryptoslip-sdk/tree/main/skills/cryptoslip)
- [CryptoSLIP Pocket Slip on ClawHub](https://clawhub.ai/naraprotocol/skills/cryptoslip)
- [CryptoSLIP slip creation](https://slip.naraprotocol.io)
- [CryptoSLIP alternate site](https://cryptoslip.eth.limo)

## Skill Output:

**Output Type(s):** [MCP tool calls, Guidance, Payment links, JSON, CSV, HTML]

**Output Format:** [Structured MCP responses, payment links, and JSON, CSV, or printable HTML receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool outputs can include payment links and transaction details; keep claim links private.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
