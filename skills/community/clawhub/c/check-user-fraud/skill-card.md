## Description: <br>
Query MySQL database to analyze user fraud/shuadan behavior. Use when user asks to check if a user is engaging in fraudulent task completion. Analyzes time intervals, publisher concentration, task duplication, and top refresh status to identify suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[star1986c](https://clawhub.ai/user/star1986c) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Risk and operations staff use this skill to investigate suspected fraudulent task completion by querying user, task, login, device, IP, account-status, and transaction records and summarizing fraud indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes reusable database credentials. <br>
Mitigation: Rotate the embedded password, remove secrets from the skill and history, and replace them with scoped read-only credentials before use. <br>
Risk: The skill can retrieve broad personal, login, device, IP, account-status, and financial data. <br>
Mitigation: Run it only with explicit authorization, role checks, case justification, audit logging, and default redaction for sensitive fields. <br>
Risk: The fraud investigation queries may exceed a tightly scoped user-fraud check. <br>
Mitigation: Limit database access to the minimum tables and records needed for the approved investigation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/star1986c/check-user-fraud) <br>
- [Fraud analysis guide](artifact/references/fraud_analysis_guide.md) <br>
- [User records query](artifact/references/query_user_records.sql) <br>
- [Top refresh query](artifact/references/query_top_refresh.sql) <br>
- [Account transactions query](artifact/references/query_account_trans.sql) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-formatted analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fraud assessments include risk level, indicator counts, detailed records, and summary conclusions when database queries return data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
