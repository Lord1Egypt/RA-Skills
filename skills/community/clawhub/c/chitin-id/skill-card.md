## Description: <br>
Permanent, verifiable identity for AI agents using ERC-8004 passports, Chitin soul certificates, on-chain certificates, and governance voting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EijiAC24](https://clawhub.ai/user/EijiAC24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to register AI agents with Chitin, create or bind ERC-8004 passports, manage soul certificates, resolve DIDs, verify other agents, and interact with Chitin certificates, governance, and MCP tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registration can create permanent public identity records and sends registration data to Chitin. <br>
Mitigation: Use review mode, inspect all public fields before submission, and proceed only with explicit owner approval. <br>
Risk: The skill includes flows involving private keys, EIP-712 signatures, certificate issuance, fleet or admin changes, spending allowances, decommissioning, and other signed write operations. <br>
Mitigation: Do not give the skill or MCP server raw wallet private keys; use a wallet, hardware signer, or host-managed signing flow, and require explicit owner approval for each signed write operation. <br>
Risk: Security evidence flags inconsistent privacy messaging about sending full system prompts to Chitin. <br>
Mitigation: Do not include sensitive prompt content unless the owner accepts Chitin receiving registration data and the selected public fields have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EijiAC24/chitin-id) <br>
- [Chitin documentation](https://chitin.id/docs) <br>
- [Chitin API reference](https://chitin.id/docs/api) <br>
- [Chitin whitepaper](https://chitin.id/whitepaper) <br>
- [Chitin skill guide](https://chitin.id/skill.md) <br>
- [Heartbeat routine](https://chitin.id/heartbeat.md) <br>
- [Skill metadata](https://chitin.id/skill.json) <br>
- [Chitin MCP documentation](https://chitin.id/docs/mcp) <br>
- [chitin-mcp-server npm package](https://www.npmjs.com/package/chitin-mcp-server) <br>
- [Chitin Certs](https://certs.chitin.id) <br>
- [Chitin Governance](https://vote.chitin.id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples, curl commands, endpoint references, and MCP setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include registration summaries, API request bodies, signature-handling guidance, verification steps, and MCP server commands.] <br>

## Skill Version(s): <br>
1.2.3 (source: server-resolved ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
