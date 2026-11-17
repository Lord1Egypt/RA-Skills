## Description:

Facilitates over-the-counter token trades between agents using Uniswap pricing and settlement tools, with ERC-8004 counterparty checks and explicit user confirmation before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to coordinate user-confirmed agent-to-agent token trades with counterparty identity checks, Uniswap pool pricing, and settlement reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real crypto trades and the security evidence warns that settlement guarantees are overstated.

Mitigation: Treat outputs as user-confirmed Uniswap swap guidance, require wallet confirmation before every transaction, and do not assume the counterparty is forced to execute.

Risk: Incorrect token addresses, chains, prices, or safety checks could cause financial loss.

Mitigation: Manually verify token addresses and chains, require a fresh safety check, compare quoted terms against current pool pricing, and stop when required trade parameters are missing.

Risk: Mutable installation commands can change what code is installed later.

Mitigation: Prefer pinned installation sources or reviewed release artifacts before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/agent-otc-trade)
- [Agentic-Uniswap MCP server](https://github.com/wpank/Agentic-Uniswap/tree/main/packages/mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-like trade reports and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include counterparty identity status, Uniswap pricing, settlement method, wallet or safety warnings, and transaction links when a trade is executed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
