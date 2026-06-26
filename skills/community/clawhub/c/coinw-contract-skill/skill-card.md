## Description: <br>
Coinw Contract REST API skill: covers market data, order placement/cancellation, TP/SL, position and order queries, account assets, position modes, and leverage queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[connectcoinw](https://clawhub.ai/user/connectcoinw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-agent operators use this skill to query CoinW futures market and account data, then prepare or execute contract-trading actions through agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires high-value CoinW API credentials for private futures endpoints. <br>
Mitigation: Use a dedicated least-privilege API key, disable withdrawals unless strictly needed, enable IP allowlisting where possible, and avoid pasting secrets into chat. <br>
Risk: The skill can perform account-changing futures actions such as placing orders, closing or reversing positions, adjusting margin, and changing position mode. <br>
Mitigation: Require explicit user confirmation before every trade, order cancellation, margin change, TP/SL change, or position-mode change. <br>
Risk: Troubleshooting output may expose sensitive keys, signatures, headers, cookies, IDs, or logs. <br>
Mitigation: Redact credentials and request metadata before sharing logs or examples. <br>
Risk: CoinW futures endpoints have per-interface and global frequency limits that can lead to throttling, temporary bans, or blacklisting. <br>
Mitigation: Throttle requests, monitor rate-limit errors, and back off when CoinW returns frequency-limit responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/connectcoinw/coinw-contract-skill) <br>
- [Authentication](references/Authentication.md) <br>
- [API Key Creation Steps](references/api-key-creation-steps.md) <br>
- [Error Code Explanation](references/error-codes.md) <br>
- [CoinW API Notes](references/notes.md) <br>
- [CoinW Futures Trading Rules](https://www.coinw.com/trading-rules) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API endpoint tables, credential setup steps, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COINW_API_KEY and COINW_SECRET_KEY for private CoinW futures endpoints.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
