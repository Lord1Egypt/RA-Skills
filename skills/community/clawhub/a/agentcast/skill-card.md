## Description: <br>
Agentcast helps developers create or link a Farcaster identity for an AI agent, register it on the ERC-8004 identity registry on Base, and connect it to the AgentCast dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebayaki](https://clawhub.ai/user/sebayaki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare an AI agent for AgentCast by setting up Farcaster profile data, linking wallet identity, and registering an ERC-8004 identity on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet private keys and signer keys for Farcaster and ERC-8004 actions. <br>
Mitigation: Use a burner or limited-funds wallet, keep secrets out of chat, logs, and shared environments, store credential files with restricted permissions, and rotate any exposed key. <br>
Risk: The scripts can submit on-chain transactions or public identity updates on Base, Optimism, Farcaster, and AgentCast. <br>
Mitigation: Verify the chain, contract address, endpoint, agent metadata, wallet balance, and intended account before running commands. <br>
Risk: Some Farcaster profile and verification flows use the AgentCast proxy by default. <br>
Mitigation: Prefer direct Neynar or API configuration when available, or explicitly approve the AgentCast proxy path before sending signed messages. <br>


## Reference(s): <br>
- [ClawHub Agentcast listing](https://clawhub.ai/sebayaki/agentcast) <br>
- [AgentCast dashboard](https://ac.800.works) <br>
- [ERC-8004 Agent Identity on Base](erc-8004-base.md) <br>
- [ERC-8004 specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [farcaster-agent skill](https://github.com/rishavmukherji/farcaster-agent) <br>
- [Farcaster EIP-712 verification](https://docs.neynar.com/docs/smart-account-verifications) <br>
- [x402 protocol](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and Node.js script invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke external Farcaster, Neynar, AgentCast, Base, and Optimism services when the user runs the commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
