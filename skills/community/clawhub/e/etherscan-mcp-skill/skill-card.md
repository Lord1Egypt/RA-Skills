## Description: <br>
Use Etherscan MCP through UXC for onchain address, token holder, transaction, and contract lookup investigations with help-first schema inspection and bearer-key authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure and run Etherscan MCP workflows through UXC for read-first onchain investigations, including address balance checks, token holder analysis, transaction inspection, and contract metadata lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Etherscan API key exposure or overbroad credential binding. <br>
Mitigation: Use a dedicated Etherscan API key, bind bearer authentication only to https://mcp.etherscan.io/mcp, and verify the credential and binding before calls. <br>
Risk: Etherscan MCP schema changes or plan-gated tools can cause failed or misleading calls. <br>
Mitigation: Inspect operation help before execution, start with one read-only chain, address, token, or transaction at a time, and handle tier-gated responses explicitly. <br>
Risk: Contract verification can behave like a write or publication action. <br>
Mitigation: Require explicit user confirmation before any contract verification action. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Etherscan MCP endpoint](https://mcp.etherscan.io/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/etherscan-mcp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uxc, network access to Etherscan MCP, and an Etherscan API key for authenticated calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
