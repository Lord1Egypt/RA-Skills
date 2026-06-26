## Description: <br>
MCP server that gives AI agents the ability to make payments, manage budgets, and handle billing -- directly from Claude Desktop, Cursor, Cline, or any MCP-compatible agent runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[up2itnow](https://clawhub.ai/user/up2itnow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure MCP-compatible agents to send USDC payments, check balances, track spending, manage payment channels, and bridge USDC across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server gives an agent ongoing private-key signing authority for USDC payments. <br>
Mitigation: Use an isolated low-balance wallet, avoid reusing production keys, and provide AGENT_PRIVATE_KEY only in a controlled environment. <br>
Risk: Under-limit transfers may execute without clear per-payment approval. <br>
Mitigation: Set very small MAX_TX_USDC and MAX_DAILY_USDC values and require explicit MCP client approval before every payment-related tool call. <br>
Risk: The release depends on an external npm package that can perform payment actions. <br>
Mitigation: Inspect or pin the package version before installation and review updates before exposing wallet credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/up2itnow/agentpay-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, JSON MCP configuration, environment variables, and tool descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node plus AGENT_PRIVATE_KEY and RPC_URL environment variables; payment behavior depends on configured MAX_TX_USDC and MAX_DAILY_USDC limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
