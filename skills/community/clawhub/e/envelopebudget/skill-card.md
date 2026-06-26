## Description: <br>
Manage budgets, transactions, accounts, envelopes, payees, and reports using the EnvelopeBudget.com API for tracking and organizing finances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djedi](https://clawhub.ai/user/djedi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect and manage EnvelopeBudget finances, including budgets, transactions, accounts, envelopes, payees, transfers, reconciliation, and spending reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change sensitive budget records using a broad EnvelopeBudget API surface. <br>
Mitigation: Require the agent to show the exact budget, account, envelope, payee or transaction IDs, amount, date, API method, and request body before any create, update, delete, transfer, reconcile, merge, archive, allocate, or bulk operation. <br>
Risk: Financial records may be changed incorrectly if the requested amount, sign, date, or destination is misunderstood. <br>
Mitigation: Confirm cents-based amounts, inflow or outflow direction, dates, and source and destination IDs before allowing write operations. <br>


## Reference(s): <br>
- [EnvelopeBudget API Reference](references/api-reference.md) <br>
- [EnvelopeBudget](https://envelopebudget.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and formatted JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ENVELOPE_BUDGET_API_KEY and uses curl plus python3 for API requests and JSON formatting.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
