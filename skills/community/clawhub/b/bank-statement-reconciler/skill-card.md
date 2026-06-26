## Description: <br>
Bank Statement Reconciler uploads bank statements in CSV, Excel, or PDF format with orders or invoices, applies automatic matching, and returns matched transactions, differences, unclaimed funds, and unmatched orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance and operations users use this skill to reconcile bank, payment-platform, and e-commerce statement files against orders or invoices and produce reviewable discrepancy reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive bank, payment, order, and invoice files and may persist reconciliation reports locally. <br>
Mitigation: Test with non-production data first, control the report output directory, and remove exported reconciliation files when they are no longer needed. <br>
Risk: PDF inputs rely on an external document parser for financial data extraction. <br>
Mitigation: Prefer CSV, Excel, or JSON inputs when possible, and use PDF inputs only when the parser is trusted and isolated. <br>
Risk: Feishu card output can share reconciliation summaries outside the local workspace. <br>
Mitigation: Do not send Feishu cards containing real bank or customer data until sharing and retention behavior is documented and approved. <br>


## Reference(s): <br>
- [Supported Formats](references/supported-formats.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/qiji0802/bank-statement-reconciler) <br>
- [Publisher Profile](https://clawhub.ai/user/qiji0802) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Guidance] <br>
**Output Format:** [Reconciliation summaries, structured result dictionaries, Excel or CSV report files, and Feishu card payloads where enabled] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include matched transactions, differences, unclaimed funds, unmatched orders, summary statistics, and an optional exported report path.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
