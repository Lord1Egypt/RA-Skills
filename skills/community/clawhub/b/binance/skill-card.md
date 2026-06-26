## Description: <br>
Operate Binance Spot APIs through safe REST, WebSocket, and SDK workflows with signed requests, rate-limit control, and testnet-first execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to work with Binance Spot market data, signed account or trading requests, WebSocket reconciliation, and troubleshooting workflows while defaulting new order activity to testnet-first validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real Binance Spot trading workflows when production endpoints and credentials are used. <br>
Mitigation: Start on testnet and require explicit confirmation for every production order. <br>
Risk: Binance API keys, signatures, balances, or full order details could be exposed if copied into chat, repository files, or local notes without care. <br>
Mitigation: Restrict API-key permissions and keep local notes free of secrets, signatures, balances, and full order details unless the user intentionally accepts that record. <br>
Risk: Rate-limit abuse or ambiguous execution status can create operational risk during trading workflows. <br>
Mitigation: Use the skill's rate-limit backoff, test order, and REST or WebSocket reconciliation guidance before retrying or promoting orders. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/binance) <br>
- [Binance Spot REST API](https://api.binance.com) <br>
- [Binance Spot Public Market Data](https://data-api.binance.vision) <br>
- [Binance Spot Testnet](https://testnet.binance.vision) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose REST or WebSocket requests, local note templates, and testnet-first validation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
