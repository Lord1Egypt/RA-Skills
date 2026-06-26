## Description: <br>
FIU MCP Market Data and Trading Assistant for querying stock quotes, K-line data, positions, cash, market analysis, and trading operations across HK, US, and CN markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ulnit](https://clawhub.ai/user/ulnit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to FIU MCP services for market data lookup, security search, account status checks, and stock trading workflows. It is most relevant when the user needs agent-assisted access to HK, US, or CN market data and trading-capable remote services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow persists a financial-service credential and updates the user's global MCP configuration. <br>
Mitigation: Use a paper-trading or least-privilege FIU token, back up and review ~/.mcp.json before setup, and confirm token files are readable only by the owner. <br>
Risk: The skill exposes trading-capable remote calls, including order placement and generic router access to trading tools. <br>
Mitigation: Keep trading in simulated mode unless a real trade is explicitly intended, review parameters before execution, and avoid generic router calls for trade, cancel, modify, or futures actions unless the user has confirmed the action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ulnit/fiu-market-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/ulnit) <br>
- [FIU MCP tools reference](docs/MCP_TOOLS.md) <br>
- [FIU MCP server interface documentation](docs/mcp-interfaces_EN.md) <br>
- [FIU token login](https://ai.szfiu.com/auth/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or terminal-oriented text with JSON API responses when invoking FIU MCP endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FIU_MCP_TOKEN and local binaries curl, jq, date, and bash for the bundled shell workflows.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
