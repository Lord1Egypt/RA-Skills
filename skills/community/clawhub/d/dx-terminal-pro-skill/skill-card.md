## Description: <br>
Manage a DX Terminal Pro trading agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[octal-crypto](https://clawhub.ai/user/octal-crypto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect a DX Terminal trading agent, review portfolio and market data, and prepare commands that can update strategies, settings, deposits, or withdrawals for the agent vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private-key commands can move funds or change live trading behavior. <br>
Mitigation: Use a dedicated low-balance wallet and keep DX_TERMINAL_PRIVATE_KEY out of chats, logs, and shared command output. <br>
Risk: Deposits, withdrawals, settings updates, and strategy changes can affect a live vault. <br>
Mitigation: Require explicit approval before execution after checking the contract address, network, method, value, and parameters. <br>


## Reference(s): <br>
- [DX Terminal](https://terminal.markets) <br>
- [ClawHub skill page](https://clawhub.ai/octal-crypto/dx-terminal-pro-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/octal-crypto) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may reference cast, curl, jq, DX_TERMINAL_PRIVATE_KEY, Base mainnet RPC, vault addresses, token addresses, wei-denominated amounts, and strategy or settings parameters.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
