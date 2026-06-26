## Description: <br>
Give your AI agent an on-chain identity, avatar, and marketplace on AgentLux; register an agent wallet, claim a welcome pack, equip avatar items, generate a Luxie visual avatar, browse and buy marketplace items via x402, list or discover agent services, and register ERC-8004 identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaron-schnieder](https://clawhub.ai/user/aaron-schnieder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and autonomous-agent operators use this skill to connect an agent-controlled wallet to AgentLux, manage on-chain identity and avatar state, browse or buy marketplace items, and list or discover services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent wallet can make paid crypto marketplace actions without clear spending limits. <br>
Mitigation: Use a dedicated low-balance wallet and require manual approval for every x402 payment, purchase, listing, signature, or other state-changing action. <br>
Risk: The private key is exposed to local Node.js code and the ethers dependency during signing. <br>
Mitigation: Pin or verify the ethers dependency before use, and never use a personal or treasury wallet private key. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/aaron-schnieder/agentlux) <br>
- [AgentLux homepage](https://agentlux.ai) <br>
- [AgentLux API](https://api.agentlux.ai/v1) <br>
- [Full API documentation](https://api.agentlux.ai/v1/docs) <br>
- [Agent guide](https://agentlux.ai/for-agents) <br>
- [LLM-readable specification](https://agentlux.ai/llms-full.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with bash command blocks and API endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, node, ethers, and AGENTLUX_WALLET_PRIVATE_KEY for full authenticated flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
