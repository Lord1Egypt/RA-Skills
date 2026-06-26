## Description: <br>
AIUSD trading and account management skill that calls backend services for balances, trading, staking, withdrawals, gas top-ups, and transaction history using local authentication tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChaunceyLiu](https://clawhub.ai/user/ChaunceyLiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and bot operators use this skill to manage AIUSD accounts through natural-language agents, including balance checks, trading, staking, withdrawals, gas top-ups, deposits, reauthentication, and transaction history review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move funds through trading, withdrawal, staking, unstaking, and gas top-up actions using locally available tokens. <br>
Mitigation: Use limited balances or limited-scope credentials where possible and require explicit user confirmation before any funds-moving action. <br>
Risk: The scanner summary flags under-scoped installer and reauthentication behavior. <br>
Mitigation: Review the embedded package before running self-extracting installers and require explicit confirmation before reauthentication. <br>
Risk: Authentication tokens are resolved from environment, OAuth, or a local token file. <br>
Mitigation: Protect local token storage, avoid shared execution environments, and rotate or clear tokens when account access changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChaunceyLiu/aiusd) <br>
- [AIUSD official website](https://aiusd.ai) <br>
- [AIUSD OAuth login](https://mcp.alpha.dev/oauth/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown and text responses with shell commands and backend tool call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live tool schemas before calls and may return account, trade, staking, withdrawal, gas, authentication, or transaction status information.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
