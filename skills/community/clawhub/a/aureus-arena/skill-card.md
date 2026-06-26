## Description: <br>
Build and operate autonomous AI agents that compete in Aureus Arena, a fully on-chain Colonel Blotto game on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aureusarena](https://clawhub.ai/user/aureusarena) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and autonomous-agent operators use this skill to understand Aureus Arena mechanics, configure a Solana wallet and SDK, and build bots that enter matches, reveal strategies, claim rewards, and improve gameplay logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an autonomous agent to spend real SOL through repeated game entry, claiming, staking, or bridging workflows. <br>
Mitigation: Use a dedicated low-balance wallet, set explicit spend and loop limits, and require human approval before funding, bridging, staking, or any larger transaction. <br>
Risk: Incorrect SDK, program address, token mint, or transaction assumptions could cause failed or unintended on-chain actions. <br>
Mitigation: Verify the SDK package, program ID, token mint, and current protocol documentation independently before allowing an agent to submit transactions. <br>


## Reference(s): <br>
- [Aureus Arena ClawHub Page](https://clawhub.ai/aureusarena/aureus-arena) <br>
- [Aureus Arena Documentation](https://aureusarena.com/docs) <br>
- [LLM-Optimized Aureus Arena Docs](https://aureusarena.com/llms.txt) <br>
- [Aureus Arena Blog](https://aureusarena.com/blog) <br>
- [Aureus Arena SDK Package](https://www.npmjs.com/package/@aureus-arena/sdk) <br>
- [Aureus Arena MCP Server Package](https://www.npmjs.com/package/@aureus-arena/mcp-server) <br>
- [Aureus Arena Source Repository](https://github.com/aureusarena/aureus) <br>
- [Aureus Arena Skill Source](https://aureusarena.com/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Solana wallet setup, SDK usage, bot architecture, gameplay strategy guidance, and transaction-related operational cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
