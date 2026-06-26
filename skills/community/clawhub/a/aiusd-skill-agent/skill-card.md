## Description: <br>
AIUSD trading and account management skill for cryptocurrency trading and account management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChaunceyLiu](https://clawhub.ai/user/ChaunceyLiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to check AIUSD balances, view trading accounts and transaction history, and prepare account, staking, withdrawal, gas top-up, and trading operations through natural language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move funds through trading, staking, gas top-ups, and withdrawals. <br>
Mitigation: Require explicit human confirmation of token, amount, destination address, network, fees, and expected result before any fund-moving action. <br>
Risk: Installers and reset flows can make broad local changes, including changes to local authentication state. <br>
Mitigation: Install only from a trusted AIUSD source, inspect the extracted package before running installers, and avoid shared hosts or machines with unrelated wallet, exchange, or API credentials. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/ChaunceyLiu/aiusd-skill-agent) <br>
- [AIUSD official website](https://aiusd.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and structured parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require live tool schema checks and explicit human confirmation before fund-moving actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
