## Description: <br>
Manage personal finances via Firefly III API. Use when user asks about budgets, transactions, accounts, categories, piggy banks, subscriptions, recurring transactions, or financial reports. Supports creating, listing, updating transactions; managing accounts and balances; setting budgets; tracking savings goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pushp1997](https://clawhub.ai/user/pushp1997) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to manage Firefly III personal finance records through its API, including accounts, transactions, budgets, categories, savings goals, subscriptions, recurring transactions, rules, tags, reports, and balances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive personal finance records from Firefly III. <br>
Mitigation: Use a limited Firefly III token when possible, store it securely, and restrict permissions on ~/.firefly_token. <br>
Risk: The skill includes create, update, delete, rule, budget, and recurring-transaction actions that can change financial records. <br>
Mitigation: Require the agent to show the exact API request and obtain explicit approval before any write action. <br>
Risk: Requests may transmit financial data to the configured Firefly III server. <br>
Mitigation: Use HTTPS for FIREFLY_URL and verify the configured server before running API commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pushp1997/firefly-iii) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples that read or modify Firefly III financial data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
