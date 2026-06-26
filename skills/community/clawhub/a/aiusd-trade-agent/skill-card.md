## Description: <br>
AIUSD trading and account management skill for balances, trades, staking, withdrawals, gas top-ups, transaction history, and authentication through an MCP backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChaunceyLiu](https://clawhub.ai/user/ChaunceyLiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to manage AIUSD accounts, check balances, execute token trades, stake or unstake AIUSD, withdraw funds, top up gas, and review transaction history from chat or CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute trades, staking actions, withdrawals, and gas top-ups that may move funds. <br>
Mitigation: Use a limited-balance account and require explicit user confirmation before every trade, withdrawal, stake, unstake, or gas top-up. <br>
Risk: Authentication tokens and chat access could enable account actions if exposed. <br>
Mitigation: Protect local tokens, restrict access to the agent environment, and independently verify login domains before authenticating. <br>
Risk: The self-extracting installers can remove or overwrite an existing aiusd-skill directory and install dependencies. <br>
Mitigation: Run installers only in a clean working directory without important local changes or secrets, and review installer behavior before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChaunceyLiu/aiusd-trade-agent) <br>
- [AIUSD website](https://aiusd.ai) <br>
- [AIUSD OAuth login](https://mcp.alpha.dev/oauth/login) <br>
- [AIUSD skill release download](https://github.com/galpha-ai/aiusd-skills/releases/download/v1.0.0/aiusd-skill-agent.skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and tool result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include account, balance, trade, staking, withdrawal, gas, authentication, and transaction-history guidance returned from backend tool calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact build-info.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
