## Description: <br>
Receipt OCR, GL code mapping, policy compliance checking, and anomaly detection for business expenses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, accounting, and operations teams use this skill to extract receipt or statement details, categorize expenses against GL codes, check expense-policy compliance, and identify transactions that need human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business receipts and expense records can contain sensitive financial or personal data. <br>
Mitigation: Use local OCR when possible, review any optional external OCR or vision API use before sending sensitive receipts, and follow internal data-handling rules. <br>
Risk: Automated GL categorization, anomaly detection, or policy checks can be incorrect. <br>
Mitigation: Keep human approval in place before posting categorized transactions, reimbursements, or accounting changes, especially for low-confidence or flagged items. <br>
Risk: The skill boundaries exclude tax filing, payroll processing, real-time bank-feed categorization without review, and legal contract work. <br>
Mitigation: Route excluded workflows to qualified reviewers, approved systems, or specialized skills instead of treating this skill as authoritative for those tasks. <br>


## Reference(s): <br>
- [GL Code Mapping Reference](references/gl-mapping.md) <br>
- [Standard Expense Policy Rules](references/policy-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce categorized receipt records, batch summaries, policy flags, confidence scores, and review recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
