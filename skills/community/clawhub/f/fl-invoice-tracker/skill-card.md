## Description: <br>
Invoice & Expense Tracker helps an agent parse natural-language invoice and expense statements into a local ledger, generate reports and spending summaries, and export CSV files for QuickBooks/Xero. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PhilipStark](https://clawhub.ai/user/PhilipStark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and small teams use this skill to record invoices, expenses, income, and payments from plain-language prompts, then review reports, spending alerts, and accounting-oriented exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and maintains local financial records that may contain sensitive business data. <br>
Mitigation: Keep ledger and export files out of public repositories and apply local access controls appropriate for financial records. <br>
Risk: Parsed entries, reports, and CSV exports may be incomplete or inaccurate for accounting, tax, or compliance use. <br>
Mitigation: Review parsed entries and exports before relying on them, and apply independent accounting or tax controls when records are material. <br>
Risk: Users may accidentally enter account numbers, card numbers, SSNs, or tax-critical records. <br>
Mitigation: Avoid entering highly sensitive identifiers and decline to store them unless separate user controls are in place. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PhilipStark/fl-invoice-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV, Files, Guidance] <br>
**Output Format:** [Markdown responses with local JSON ledger updates and CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local financial records in the workspace; users should review entries and exports before relying on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
