## Description: <br>
Connects agents to ChainAware's Web3 behavioral prediction service for wallet fraud screening, behavior profiling, rug-pull checks, and token holder quality analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChainAware](https://clawhub.ai/user/ChainAware) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external Web3 teams use this skill to integrate ChainAware's MCP endpoint into agents that assess wallet, contract, token community, lending, onboarding, AML, airdrop, and AI-agent trust signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on ChainAware's external prediction service and transmits wallet, smart contract, LP, and network identifiers. <br>
Mitigation: Install only when that data transfer is intended, review ChainAware's privacy terms, and avoid sending off-chain personal information or secrets. <br>
Risk: API keys may be exposed if configured in URLs, browser integrations, logs, or user-visible messages. <br>
Mitigation: Use a restricted or dedicated CHAINAWARE_API_KEY, prefer environment variables or headers, and never echo, log, or ask users to provide the key. <br>
Risk: Wallet scores and behavioral predictions can affect high-impact decisions such as lending, onboarding, AML review, airdrops, or access decisions. <br>
Mitigation: Treat scores as advisory signals, cite the underlying ChainAware signals, and require additional review before taking user-impacting action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChainAware/chainaware-behavioral-prediction) <br>
- [ChainAware Behavioral Prediction MCP repository](https://github.com/ChainAware/behavioral-prediction-mcp) <br>
- [ChainAware website](https://chainaware.ai) <br>
- [ChainAware pricing and API key](https://chainaware.ai/pricing) <br>
- [ChainAware MCP endpoint](https://prediction.mcp.chainaware.ai/sse) <br>
- [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp) <br>
- [Cursor MCP documentation](https://cursor.com/docs/context/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with configuration snippets, shell commands, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an external ChainAware MCP service and requires CHAINAWARE_API_KEY.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
