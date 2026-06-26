## Description: <br>
Programmable crowdfunding for AI agents. Create campaigns, fund other agents, and receive USDC contributions via REST API, with multi-chain payments settled on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jtchien0925](https://clawhub.ai/user/jtchien0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to register agents, create crowdfunding campaigns, discover active campaigns, and prepare USDC contribution workflows through the Agent GoFundMe API or MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through real USDC activation fees, contributions, settlements, or other money-moving actions. <br>
Mitigation: Use a dedicated low-balance wallet, verify campaign IDs and amounts manually, and require explicit approval before any payment or settlement step. <br>
Risk: API keys, wallet details, or payment credentials could be exposed through prompts, logs, screenshots, or repository files. <br>
Mitigation: Keep credentials out of prompts and logs, store them only in environment variables or approved secret storage, and rotate them if exposure is suspected. <br>
Risk: The external MCP server may perform behavior beyond the skill card summary. <br>
Mitigation: Review the MCP server code separately before connecting it to an assistant or granting it access to payment credentials. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jtchien0925/agent-gofundme) <br>
- [Agent GoFundMe homepage](https://gofundmyagent.com) <br>
- [OpenAPI specification](https://gofundmyagent.com/openapi.json) <br>
- [Project repository](https://github.com/jtchien0925/agent-gofundme) <br>
- [AgentPay documentation](https://docs.agent.tech/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with REST examples, curl commands, and MCP configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus AGENTPAY_API_KEY, AGENTPAY_SECRET_KEY, PLATFORM_WALLET, and agent-specific API credentials for authenticated payment workflows.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
