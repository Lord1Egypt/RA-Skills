## Description:

Helps developers implement and review Hyperliquid integrations for market data, accounts, orders, signing, streams, risk controls, and reconciliation without choosing trades or executing account actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to design, implement, or review Hyperliquid adapters, watchers, bots, and tests with explicit authorization and failure handling. It does not select trades or authorize account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signer credentials or account authority could be exposed during integration work.

Mitigation: Keep private keys outside the agent and repository; use a separate trusted signer.

Risk: A development or test action could affect an account without consent.

Mitigation: Use read-only checks by default and require explicit approval before any testnet write; never send mainnet actions during ordinary validation.

Risk: Optional dependency installation could introduce unreviewed code.

Mitigation: Review optional npx installation commands before running them.

## Reference(s):

- [Hyperliquid Engineer on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-hyperliquid-engineer)
- [Adapter architecture](artifact/references/adapter-architecture.md)
- [Security invariants](artifact/references/security-invariants.md)
- [Hyperliquid API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
- [Hyperliquid Python SDK](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Code and Markdown with implementation and validation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports supported contracts, test results, unsupported actions, and residual risk.]

## Skill Version(s):

0.4.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
