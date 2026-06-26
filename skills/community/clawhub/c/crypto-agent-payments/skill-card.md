## Description: <br>
Create and manage ERC20 wallets, transfer and swap tokens across supported chains, enable agent payments, and earn referrer fees in AI agent ecosystems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicofains1](https://clawhub.ai/user/nicofains1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure crypto wallet and payment workflows for transfers, swaps, bounties, rewards, and agent-to-agent payouts. It is intended for users who can safely manage private keys, token approvals, and irreversible blockchain transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent-accessible hot wallet through an external MCP package and can expose funds if a main wallet private key is used. <br>
Mitigation: Use a new low-balance wallet, avoid main wallet private keys, and review or pin the MCP package where possible. <br>
Risk: Transfers, swaps, approvals, slippage settings, recipient addresses, chains, amounts, and referral fees can result in irreversible fund movement. <br>
Mitigation: Confirm every transaction detail before acting, start with small test amounts, and revoke token approvals after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicofains1/crypto-agent-payments) <br>
- [@onlyswaps/mcp-server npm package](https://www.npmjs.com/package/@onlyswaps/mcp-server) <br>
- [OnlySwaps docs](https://onlyswaps.fyi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, JSON configuration snippets, and MCP tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some wallet operations require a PRIVATE_KEY, funded wallet, user confirmation, and careful review of transaction details before execution.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
