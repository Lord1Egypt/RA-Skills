## Description:

Helps run a USDC payroll on Base through Spraay, validating the roster locally and requiring separate approvals before sharing data, paying for the gateway call, and signing transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Payroll operators and finance teams use this skill to validate a roster of employee and contractor wallet addresses and amounts, then prepare and approve a USDC payroll payment on Base. It is not for general payroll advice, tax work, or unrelated payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and payment amounts become public on-chain, exposing sensitive payroll information.

Mitigation: Share only wallet addresses and amounts, and obtain explicit user approval before sending the roster to the gateway.

Risk: Completed blockchain payments cannot be reversed if a recipient, amount, or transaction is wrong.

Mitigation: Validate the roster locally, review the decoded transactions against it, and require explicit approval before signing.

Risk: A paid gateway request incurs a fee.

Mitigation: Show the endpoint and $0.10 price and obtain a separate approval before the paid call.

Risk: Sharing wallet secrets could compromise funds.

Mitigation: Never provide, read, or store private keys or seed phrases; sign through the treasury wallet's own software.

## Reference(s):

- [Spraay Protocol documentation](https://docs.spraay.app)
- [Spraay Protocol](https://spraay.app)
- [Spraay x402 discovery](https://gateway.spraay.app/.well-known/x402.json)
- [Spraay MCP server](https://smithery.ai/servers/Plagtech/Spraay-x402-mcp)
- [ClawHub skill release](https://clawhub.ai/plagtech/skills/crypto-payroll)

## Skill Output:

**Output Type(s):** [JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown with JSON and JavaScript examples, validation summaries, and transaction review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires distinct approvals before data sharing, paid API use, and transaction signing; reports payment only after on-chain confirmation.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
