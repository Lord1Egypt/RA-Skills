## Description: <br>
Access Futu stock market data via an MCP server, including real-time quotes, K-lines, options, and account information for HK, US, and CN markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuizhengqi1](https://clawhub.ai/user/shuizhengqi1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Futu OpenD through the futu-stock MCP server for market-data lookup, screening, subscriptions, options queries, and brokerage-account information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access brokerage-account data through Futu OpenD. <br>
Mitigation: Connect only to a trusted Futu OpenD instance, keep account access scoped to the intended environment, and disable position access when it is not needed. <br>
Risk: Trading-related capabilities can create live-account financial risk if enabled. <br>
Mitigation: Keep FUTU_ENABLE_TRADING=0 unless trading is deliberately required, prefer FUTU_TRADE_ENV=SIMULATE for testing, and review all trade-impacting actions before use. <br>
Risk: The skill depends on the external futu-stock MCP server package. <br>
Mitigation: Install only a trusted or pinned version of the server package and use an isolated Python environment for dependency installation. <br>
Risk: Automatic OpenD startup can launch a local brokerage connectivity service. <br>
Mitigation: Leave OPEND_PATH unset unless automatic startup is intended and the configured OpenD path has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuizhengqi1/futu-stock) <br>
- [Publisher profile](https://clawhub.ai/user/shuizhengqi1) <br>
- [Futu OpenD command documentation](https://openapi.futunn.com/futu-api-doc/opend/opend-cmd.html) <br>
- [futu-stock MCP server](https://github.com/shuizhengqi1/futu-stock-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples and shell command snippets; MCP tool calls return JSON or text responses from the Futu server.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, futu-mcp-server, FUTU_HOST, FUTU_PORT, and a reachable Futu OpenD service.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
