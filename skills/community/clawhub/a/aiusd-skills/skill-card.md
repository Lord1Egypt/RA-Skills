## Description: <br>
Manage AIUSD accounts and trades: check balances, execute buy/sell/swap orders, stake or unstake, withdraw funds, top up gas, and view transaction history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChaunceyLiu](https://clawhub.ai/user/ChaunceyLiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an assistant manage AIUSD account workflows, including balances, trades, staking, withdrawals, gas top-ups, deposits, and transaction history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assistant-mediated trades, staking, unstaking, withdrawals, and gas top-ups can move funds. <br>
Mitigation: Require explicit approval before every financial action and verify the amount, asset, chain, destination address, and fees. <br>
Risk: Persistent account tokens and reauthentication flows can affect local auth and session state. <br>
Mitigation: Use only trusted account tokens, keep them local, and warn users that reauthentication can delete local auth or session files. <br>
Risk: Self-extracting installers run bundled code with limited user control. <br>
Mitigation: Inspect the extracted package before running installers and install only when the publisher and package are trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ChaunceyLiu/aiusd-skills) <br>
- [AIUSD official website](https://aiusd.ai) <br>
- [AIUSD OAuth login](https://mcp.alpha.dev/oauth/login) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with shell commands and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call MCP-backed tools that execute account, trading, staking, withdrawal, gas top-up, and transaction-history operations.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
