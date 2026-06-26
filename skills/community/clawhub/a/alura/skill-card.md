## Description: <br>
Integrates agents with the Alura Trading testnet API for wallet authentication, trading sessions, market data, leaderboard, referrals, and USDC verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evilboyajay](https://clawhub.ai/user/evilboyajay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call the Alura Trading testnet API for authenticated wallet flows, trading-session management, market indicators, leaderboard data, referrals, and USDC verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables authenticated trading actions and funds-transfer operations such as closing positions, withdrawals, reward claims, and USDC transfers. <br>
Mitigation: Require explicit user confirmation before any trade, close-position, withdrawal, reward claim, or USDC transfer, including the exact asset, amount, position or session ID, and destination. <br>
Risk: The skill requires wallet signatures and Bearer tokens for authenticated API use. <br>
Mitigation: Verify the official Alura testnet domain before signing wallet messages or sharing Bearer tokens. <br>


## Reference(s): <br>
- [Alura API Swagger Docs](https://testnet-api.alura.fun/api/docs) <br>
- [Alura Skill Page](https://clawhub.ai/evilboyajay/alura) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, code, shell commands, configuration] <br>
**Output Format:** [Markdown with HTTP examples, JSON payloads, and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated trading or funds-transfer API requests that require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
