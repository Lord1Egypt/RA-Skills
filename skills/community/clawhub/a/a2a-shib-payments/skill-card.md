## Description:

A framework-agnostic A2A payment agent that helps agents send SHIB on Polygon and manage escrow, price negotiation, and reputation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcus20232023](https://clawhub.ai/user/marcus20232023)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this skill to add SHIB payment, escrow-style deal tracking, price negotiation, and reputation flows to A2A-compatible agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default agent can execute SHIB transfers without authentication if deployed with a funded wallet.

Mitigation: Require authentication and per-request authorization on every transfer path before using real funds.

Risk: Wallet credentials and hot-wallet balances can expose funds if they are printed, stored in plaintext, or overfunded.

Mitigation: Use a low-balance hot wallet, protect credentials, and stop printing or plaintext-storing private keys and API credentials.

Risk: The escrow feature may function as an off-chain tracker unless it verifies or controls funds on-chain.

Mitigation: Treat escrow as tracking-only until on-chain fund control and verification are reviewed and tested.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marcus20232023/skills/a2a-shib-payments)
- [README](README.md)
- [Integration Examples](INTEGRATION-EXAMPLES.md)
- [Escrow and Negotiation Guide](ESCROW-NEGOTIATION-GUIDE.md)
- [Production Hardening](PRODUCTION-HARDENING.md)
- [Deployment Guide](DEPLOYMENT.md)
- [A2A Protocol](https://a2a-protocol.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm; payment actions can interact with a configured Polygon wallet.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
