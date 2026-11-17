## Description:

An accounts payable agent that processes supplier payments, contractor invoices, and recurring bills across crypto, fiat, and stablecoin payment rails through MCP-integrated payment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lihangmissu](https://clawhub.ai/user/lihangmissu)

### License/Terms of Use:

MIT-0

## Use Case:

Finance operations teams and workflow agents use this skill to manage accounts payable activity, including vendor payments, contractor invoices, recurring bills, audit records, approvals, and payment exception handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for real autonomous payments, so excessive credential scope or weak approval boundaries could allow unintended funds movement.

Mitigation: Use narrowly scoped payment credentials, server-side spend limits, explicit approval thresholds, and a restricted runtime environment.

Risk: Raw inter-agent requests or scheduled records could influence payment recipients or amounts if accepted without validation.

Mitigation: Require independent validation of recipient, amount, invoice reference, vendor approval status, and idempotency before executing a payment.

Risk: Payment dependency execution is security-sensitive and should not be installed or invoked without package verification.

Mitigation: Pin and verify the MCP package before use, then review the skill carefully before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lihangmissu/skills/accounts-payable-agent)
- [AgenticBTC MCP documentation](https://agenticbtc.io)
- [agenticbtc-mcp npm package](https://www.npmjs.com/package/agenticbtc-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline TypeScript, bash, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment workflow steps, configuration examples, audit summaries, exception handling guidance, and tool-call-oriented code examples.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
