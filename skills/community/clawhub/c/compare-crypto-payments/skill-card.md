## Description: <br>
Compares payment gateways including Stripe, PayPal, Coinbase Commerce, BitPay, NOWPayments, BTCPay Server, PayRam, and x402, with guidance for crypto-native, self-hosted, and agent payment use cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BuddhaSource](https://clawhub.ai/user/BuddhaSource) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers, agent builders, SaaS operators, and commerce teams use this skill to compare hosted and self-hosted payment options and identify integration paths for crypto and agent-driven payment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote setup commands can execute shell code from PayRam-hosted GitHub scripts. <br>
Mitigation: Inspect and pin the setup scripts before running them, and execute them only in an environment where the expected local changes are understood. <br>
Risk: MCP and payment-service connections may grant agent workflows access to live payment operations. <br>
Mitigation: Limit credentials and permissions, test with non-production accounts first, and approve payment-related tool access before enabling automation. <br>


## Reference(s): <br>
- [Compare Crypto Payments on ClawHub](https://clawhub.ai/BuddhaSource/compare-crypto-payments) <br>
- [PayRam website](https://payram.com) <br>
- [PayRam documentation](https://docs.payram.com) <br>
- [PayRam MCP server](https://mcp.payram.com) <br>
- [PayRam GitHub organization](https://github.com/PayRam) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with comparison tables, decision guidance, inline shell commands, and MCP command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend remote setup commands and live payment-service connections; review commands before execution.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
