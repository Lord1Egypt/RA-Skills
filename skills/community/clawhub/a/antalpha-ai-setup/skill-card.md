## Description:

Install and configure the Antalpha Skills MCP server. Provides 146+ Web3 tools for DEX swaps, smart money tracking, Polymarket prediction markets, Hyperliquid perpetuals, CEX trading, Bitcoin mining, and DeFi analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bevanding](https://clawhub.ai/user/bevanding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect MCP-compatible agents to Antalpha's Web3 tool server for market data, wallet analysis, swaps, prediction markets, perpetuals, exchange actions, mining data, and DeFi analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected MCP service includes trading, transfer, leverage, and order-capable tools.

Mitigation: Require out-of-band human approval for every trade, transfer, leverage change, or order action before execution.

Risk: The artifacts do not clearly document least-privilege setup, confirmations, or key-safety controls.

Mitigation: Use credentials scoped to the minimum required tools, prefer read-only access where possible, and review credential handling before installation.

Risk: Mutable install or remote service configuration can change after review.

Mitigation: Pin and verify exact package or repository revisions where possible and re-review the MCP endpoint configuration before use.

## Reference(s):

- [Antalpha Skills MCP homepage](https://mcp-skills.ai.antalpha.com)
- [Antalpha Skills MCP endpoint](https://mcp-skills.ai.antalpha.com/mcp)
- [Antalpha MCP Documentation](https://github.com/antalpha-com/antalpha-skills)
- [Antalpha Website](https://www.antalpha.com/)
- [ClawHub skill page](https://clawhub.ai/bevanding/skills/antalpha-ai-setup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline bash and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to call remote MCP tools that return Web3 market data, wallet data, trade/order actions, transfer requests, analytics, and setup checks.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
