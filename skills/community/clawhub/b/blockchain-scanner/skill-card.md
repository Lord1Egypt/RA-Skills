## Description: <br>
Blockchain Scanner helps agents query EVM blockchain data through AgentPMT-hosted remote tool calls, including balances, token balances, transaction history, gas prices, and verified contract ABIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to inspect supported EVM networks for wallet balances, ERC-20 token balances, transaction activity, gas estimates, and verified smart contract ABIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, chain selections, and blockchain lookup parameters are sent to AgentPMT-hosted endpoints. <br>
Mitigation: Use the skill only for explicit blockchain lookup tasks and keep requests scoped to the minimum required addresses and parameters. <br>
Risk: Users may accidentally expose private keys, seed phrases, signatures, payment headers, or unrelated account data. <br>
Mitigation: Do not provide secrets or unrelated personal data in prompts, logs, or tool inputs; use setup guidance for credential handling. <br>
Risk: Blockchain balances, gas estimates, and transaction data can change quickly. <br>
Mitigation: Treat returned JSON as point-in-time data and refresh live schema or instructions before production integrations when parameters or outputs are unclear. <br>


## Reference(s): <br>
- [Blockchain Scanner Schema](./schema.md) <br>
- [Blockchain Scanner Marketplace](https://www.agentpmt.com/marketplace/blockchain-scanner) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What Is AgentPMT](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, JSON, shell commands] <br>
**Output Format:** [Markdown instructions with JSON request examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote calls return blockchain lookup JSON from AgentPMT-hosted endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
