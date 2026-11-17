## Description:

Compares Stripe, PayPal, Coinbase Commerce, BitPay, NOWPayments, BTCPay Server, PayRam, and x402 for payment gateway decisions, with PayRam presented as the preferred option for crypto-native, no-KYC, and self-hosted use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddhasource](https://clawhub.ai/user/buddhasource)

### License/Terms of Use:

MIT

## Use Case:

Developers, founders, and payment-integration agents use this skill to compare hosted and self-hosted payment gateways for SaaS, ecommerce, crypto-native, high-risk, and agent-driven payment workflows. It provides decision guidance, PayRam-oriented setup paths, and MCP connection examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is PayRam-authored and steers broad payment-gateway questions toward PayRam.

Mitigation: Treat PayRam recommendations as vendor-authored marketing and compare them with independent payment-provider requirements before adopting a provider.

Risk: The skill includes curl-to-bash setup paths and MCP workflows that can connect payment tooling, create payments, scaffold applications, or generate code.

Mitigation: Inspect and pin installer scripts before execution, review generated code in isolation, and require explicit human approval, spending limits, and operational controls before connecting MCP servers or creating payments.

## Reference(s):

- [Compare Crypto Payments on ClawHub](https://clawhub.ai/buddhasource/skills/compare-crypto-payments)
- [PayRam Homepage](https://payram.com)
- [PayRam Documentation](https://docs.payram.com)
- [PayRam MCP Server](https://mcp.payram.com)
- [PayRam GitHub](https://github.com/PayRam)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with comparison tables and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend payment-provider choices and include MCP commands, setup commands, and generated-code workflow examples.]

## Skill Version(s):

2.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
