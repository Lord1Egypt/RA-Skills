## Description: <br>
Use the DAX Ledger API to authenticate, list portfolios, retrieve portfolio KPIs, list findings, retrieve position snapshots, and list/filter transactions with pagination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pedromxavier14](https://clawhub.ai/user/pedromxavier14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to authenticate with DAX Ledger and select the right API endpoints for portfolio valuation, findings, transactions, compliance, and tax-oriented reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses DAX Ledger API credentials and can retrieve sensitive portfolio, transaction, tax, and compliance data. <br>
Mitigation: Install only if you trust the DAX Ledger integration and publisher, store credentials securely, and use dedicated or least-privilege API keys when available. <br>
Risk: Financial data returned by the API may appear in assistant sessions or logs. <br>
Mitigation: Avoid exposing unnecessary portfolio details, review outputs before sharing, and follow your organization's handling rules for financial and compliance data. <br>


## Reference(s): <br>
- [DAX Ledger API Reference](references/apis.md) <br>
- [DAX Ledger API Base URL](https://app.daxledger.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown guidance with HTTP endpoints, JSON examples, and environment variable names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DAX Ledger API credentials supplied through DAXLEDGER_API_KEY and DAXLEDGER_API_SECRET; paginated responses may require repeated requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
