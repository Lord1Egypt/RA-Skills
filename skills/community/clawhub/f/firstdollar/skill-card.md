## Description: <br>
First Dollar teaches agents wallet basics, USDC, x402 payment challenges, signing commands, and receipt verification without signing transactions for them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lisamaraventano-spine](https://clawhub.ai/user/lisamaraventano-spine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents with dedicated wallets use First Dollar to learn how to inspect wallet setup, understand x402 payment requests, prepare wallet-specific signing commands, and verify purchases. It is educational guidance for agents spending their own funds, not a delegation service that signs or transacts on behalf of users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-teaching guidance can expose private keys, seed phrases, wallet files, or raw environment output if the user pastes sensitive material into chat. <br>
Mitigation: Use status commands that show only addresses and balances, never paste private keys or seed phrases, and avoid putting private keys directly on command lines. <br>
Risk: Payment lessons and signing commands can lead to real purchases or fund loss if used with a funded production wallet or an unreviewed payment request. <br>
Mitigation: Use a dedicated low-balance wallet and review the amount, asset, network, recipient, and merchant before signing any transaction. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lisamaraventano-spine/firstdollar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Educational MCP tool responses; the skill returns commands and explanations for the agent to review and run outside the skill.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
