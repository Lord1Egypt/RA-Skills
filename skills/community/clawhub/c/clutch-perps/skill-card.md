## Description:

Runs agentic trading workflows on Clutch Perps through MCP for setup, live trade workflows, market checks, order planning, risk setup, and execution on dex.clutch.market with brokerId clutch-markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simplefarmer69](https://clawhub.ai/user/simplefarmer69)

### License/Terms of Use:


## Use Case:

Developers and external traders using MCP-enabled agents use this skill to set up and operate Clutch Perps workflows. It supports venue-locked market checks, order planning, risk framing, and approval-gated execution for dex.clutch.market on Arbitrum One.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external MCP install path uses npx, which can execute remote code and creates a supply-chain risk when unpinned.

Mitigation: Verify the npm package and repository before installing, prefer an exact reviewed version instead of @latest, and run without administrator privileges.

Risk: Trade execution can create unintended financial exposure if broker, venue, size, leverage, TP/SL, or risk cap differ from the user's intent.

Mitigation: Do not approve trade execution unless broker, venue, size, leverage, TP/SL, and risk cap match the user's intent.

Risk: Execution-ready trading steps can be misused if treated as autonomous always-on trading without user confirmation.

Mitigation: Use the skill's approval gate and require an explicit APPROVE signal before execution-ready steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simplefarmer69/skills/clutch-perps)
- [npm package @clutchmarkets/mcp-server](https://www.npmjs.com/package/@clutchmarkets/mcp-server)
- [Clutch MCP documentation](https://nft.clutch.market/mcp)
- [Clutch MCP repository](https://github.com/clutchmarkets/clutch-mcp)
- [Clutch MCP issue tracker](https://github.com/clutchmarkets/clutch-mcp/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline text, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before execution-ready steps; enforces brokerId clutch-markets and venue dex.clutch.market.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
