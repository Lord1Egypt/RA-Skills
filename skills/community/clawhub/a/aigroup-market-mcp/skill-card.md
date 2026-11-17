## Description:

AIGroup Market MCP routes China-market and Tushare-oriented requests for A-share, index, sector, fund-flow, margin, block-trade, fund, convertible-bond, macro, and finance-news data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackdark425](https://clawhub.ai/user/jackdark425)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to route China-market research requests to the aigroup-market-mcp server for equity, index, fund, macroeconomic, flow, margin, block-trade, and news data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches an unpinned npm MCP server with npx.

Mitigation: Pin aigroup-market-mcp to a reviewed version before installation or deployment.

Risk: The MCP server requires a TUSHARE_TOKEN service token.

Mitigation: Pass only the minimum required environment to the process and rotate TUSHARE_TOKEN if exposure is suspected.

Risk: The skill allows implicit invocation of the MCP server.

Mitigation: Require explicit approval before automatic MCP invocation in sensitive workflows.

## Reference(s):

- [Market MCP Capabilities](references/capabilities.md)
- [Project homepage](https://github.com/jackdark425/aigroup-market-mcp)
- [ClawHub skill page](https://clawhub.ai/jackdark425/skills/aigroup-market-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown guidance and MCP tool results, with returned data format depending on the selected market-data operation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TUSHARE_TOKEN environment variable for the MCP server.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
