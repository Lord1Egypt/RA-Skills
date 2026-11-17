## Description:

Spending controls for AI agents that pay online via x402. Set limits, require human approval, audit every payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmrtn](https://clawhub.ai/user/nmrtn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use blacktea to enforce spending policies, approval gates, and audit logging when an agent might pay for x402-enabled APIs, data feeds, or other online resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real wallet private key can authorize x402 USDC payments.

Mitigation: Use a dedicated low-balance wallet, avoid storing valuable keys in shared agent configuration, and require human approval for meaningful charges.

Risk: The MCP server is installed through an unpinned remote npm command.

Mitigation: Pin and verify the package version where possible before enabling live payments.

Risk: Policy mistakes can allow unintended spending.

Mitigation: Start with BLACKTEA_RAIL=mock, test the approval flow, and use strict hard limits in BLACKTEA_POLICY.

## Reference(s):

- [blacktea repository](https://github.com/nmrtn/blacktea)
- [blacktea MCP package](https://www.npmjs.com/package/@nmrtn/blacktea-mcp)
- [Policy cookbook](https://github.com/nmrtn/blacktea/blob/main/docs/policy-cookbook.md)
- [ClawHub skill page](https://clawhub.ai/nmrtn/skills/blacktea)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples; MCP tools return structured payment status, receipt, and audit data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a terminal-accessible MCP setup and an EVM_PRIVATE_KEY for live x402 payments; BLACKTEA_POLICY can point to a spending-policy JSON file.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
