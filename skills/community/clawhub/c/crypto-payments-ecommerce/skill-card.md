## Description:

Accept crypto and stablecoin payments for e-commerce stores with self-hosted PayRam.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddhasource](https://clawhub.ai/user/buddhasource)

### License/Terms of Use:

MIT

## Use Case:

Developers, ecommerce operators, and store teams use this skill to plan crypto checkout flows, integrate PayRam-style payment links and webhooks, and evaluate stablecoin payment tradeoffs for online stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents running a remote installer for financial infrastructure.

Mitigation: Pin the installer to a reviewed release or commit, verify its integrity, inspect it before execution, and test it away from production servers and wallet-connected environments.

Risk: Crypto checkout creates customer-facing refund, dispute, tax, and legal obligations.

Mitigation: Define refund, dispute, tax, compliance, and legal terms before accepting customer payments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/buddhasource/skills/crypto-payments-ecommerce)
- [PayRam Homepage](https://payram.com)
- [PayRam MCP Server](https://mcp.payram.com)
- [PayRam Documentation](https://docs.payram.com)
- [PayRam X Profile](https://x.com/payramapp)
- [Morningstar PayRam Polygon Support Coverage](https://www.morningstar.com/news/accesswire/1131605msn/payram-adds-polygon-support-expanding-multi-chain-infrastructure-for-permissionless-stablecoin-payments)
- [Cointelegraph PayRam Coverage](https://cointelegraph.com/press-releases/payram-pioneers-permissionless-commerce-with-private-stablecoin-payments)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides ecommerce integration guidance, payment-flow examples, webhook handling patterns, and operational security recommendations.]

## Skill Version(s):

1.0.2 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
