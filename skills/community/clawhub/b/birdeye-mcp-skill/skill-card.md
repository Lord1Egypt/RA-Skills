## Description: <br>
Use Birdeye MCP through UXC for token market data, trending and discovery workflows, price monitoring, and DEX-related reads with help-first live tool discovery and API-key auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure authenticated Birdeye MCP access through UXC, inspect live tool help, and run read-heavy token market, discovery, price monitoring, and DEX context workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local UXC command and an API-key credential binding for a remote MCP endpoint. <br>
Mitigation: Verify the UXC command in PATH is trusted, use a minimally scoped Birdeye API key, and confirm the binding targets only mcp.birdeye.so/mcp before running operations. <br>
Risk: Birdeye MCP is described as beta, so the live tool list and argument names may change. <br>
Mitigation: Inspect host help and operation help before each new workflow, keep initial scopes narrow, and avoid hardcoding live tool assumptions. <br>
Risk: Market and discovery queries can return broad datasets that may be misread or overused in automation. <br>
Mitigation: Start with focused token, pair, chain, or market-slice scopes and parse the stable JSON envelope before using data fields downstream. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Birdeye MCP endpoint](https://mcp.birdeye.so/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/birdeye-mcp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-field guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses help-first live tool discovery and expects callers to parse the JSON envelope fields ok, kind, protocol, data, and error.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
