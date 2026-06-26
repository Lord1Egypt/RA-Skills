## Description: <br>
DailyExpenseTracker API integration for recording expenses, checking balances, and managing transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gurpreetkaits](https://clawhub.ai/user/gurpreetkaits) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to DailyExpenseTracker for recording expenses, viewing transactions, checking wallet balances, and retrieving categories through the DailyExpenseTracker API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive expense data to DailyExpenseTracker and create or modify financial records. <br>
Mitigation: Require explicit confirmation before POST or update actions that create or change expense records. <br>
Risk: The DET bearer token grants access to the user's DailyExpenseTracker account. <br>
Mitigation: Treat the token like a password, store it only in configuration, and confirm the destination domain before use. <br>
Risk: Cached wallet IDs can become stale when accounts or wallets change. <br>
Mitigation: Review and clear any local wallet-ID cache when accounts or wallets change. <br>


## Reference(s): <br>
- [DailyExpenseTracker ClawHub release](https://clawhub.ai/gurpreetkaits/det) <br>
- [DailyExpenseTracker API base URL](https://dailyexpensetracker.in/api) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a DET bearer token and may read or create DailyExpenseTracker wallet, category, and transaction records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
