## Description: <br>
Agent-to-Agent payments on TRON. Use when an agent needs to pay another agent, escrow funds, check credit scores, or verify on-chain identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ypeng1620-beep](https://clawhub.ai/user/ypeng1620-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to make TRON-based agent-to-agent payments, manage escrow, check counterparty credit, calculate protocol fees, and verify on-chain identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move funds using a TRON private key. <br>
Mitigation: Install only with a dedicated low-balance wallet, prefer testnet first, and require explicit human confirmation before payment, escrow release, or refund. <br>
Risk: Incorrect network, recipient, token, amount, or transaction details can result in unintended transfers. <br>
Mitigation: Verify the network, recipient, token, amount, and transaction details before signing. <br>
Risk: Leaked wallet credentials can enable unauthorized fund movement. <br>
Mitigation: Never commit, log, or share A2A_PRIVATE_KEY. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ypeng1620-beep/em-a2a) <br>
- [npm Package: @poisonpyf/a2a-mcp](https://www.npmjs.com/package/@poisonpyf/a2a-mcp) <br>
- [TRON Shasta Faucet](https://www.trongrid.io/shasta) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON configuration and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires A2A_NETWORK and A2A_PRIVATE_KEY environment variables for the MCP server.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
