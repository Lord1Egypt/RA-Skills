## Description: <br>
Use `aigroup-fmp-mcp` for listed-equity data from Financial Modeling Prep, including quotes, company profiles, statements, ratios, sector context, and calendar requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to route listed-equity research requests to Financial Modeling Prep data, including ticker lookup, quotes, profiles, financial statements, ratios, market context, technical indicators, and calendar information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the referenced aigroup-fmp-mcp MCP server and may require API keys or permissions. <br>
Mitigation: Verify the MCP server source is trusted and review any requested credentials or permissions before use. <br>
Risk: Market data can be time-sensitive or stale if dates are omitted. <br>
Mitigation: State quote, chart, calendar, and financial statement dates clearly in generated responses. <br>


## Reference(s): <br>
- [FMP MCP Capabilities](references/capabilities.md) <br>
- [aigroup-fmp-mcp homepage](https://github.com/jackdark425/aigroup-fmp-mcp) <br>
- [ClawHub skill page](https://clawhub.ai/jackdark425/aigroup-fmp-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, Markdown] <br>
**Output Format:** [Markdown or plain text responses using MCP-retrieved market data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke the aigroup-fmp-mcp MCP server; responses should state dates clearly for quotes, charts, and calendars.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
