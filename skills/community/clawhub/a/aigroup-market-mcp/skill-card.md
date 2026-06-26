## Description: <br>
Use `aigroup-market-mcp` for China-market and Tushare-oriented data, including A-share, index, sector, fund-flow, margin, block-trade, fund, convertible-bond, macro, and finance-news data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to route China-market questions to an MCP server for equities, indexes, market flows, funds, convertible bonds, macroeconomic data, and finance news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external npm MCP server. <br>
Mitigation: Confirm the `aigroup-market-mcp` npm package is trusted before installation or execution. <br>
Risk: The skill uses a Tushare API token. <br>
Mitigation: Use a Tushare token with only the access you are comfortable granting. <br>


## Reference(s): <br>
- [AIGroup Market MCP on ClawHub](https://clawhub.ai/jackdark425/aigroup-market-mcp) <br>
- [Market MCP Capabilities](references/capabilities.md) <br>
- [AIGroup Market MCP Homepage](https://github.com/jackdark425/aigroup-market-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional inline commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on the external npm MCP server and a configured TUSHARE_TOKEN.] <br>

## Skill Version(s): <br>
0.1.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
