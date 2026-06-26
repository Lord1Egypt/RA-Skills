## Description: <br>
Reconciles data sources using stable identifiers such as Pay Number and driver document numbers, then produces exception reporting and no silent failure checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KOwl64](https://clawhub.ai/user/KOwl64) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and data quality analysts use this skill to reconcile payroll, compliance, or weekly operational exports and get explicit reasons for missing records, duplicates, mismatches, or invalid keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input datasets and exception reports may contain sensitive identifiers such as pay numbers, names, and driver document numbers. <br>
Mitigation: Provide only the datasets needed for the reconciliation, treat generated exception reports as sensitive, and review access before sharing outputs. <br>
Risk: Incorrect matching rules or thresholds can misclassify records or stop a pipeline unexpectedly. <br>
Mitigation: Confirm key priority, field mappings, normalization rules, and tolerance thresholds before relying on the reconciliation results. <br>
Risk: Exception reports may be mistaken for approved source-system corrections. <br>
Mitigation: Use the reports for review and keep the workflow read-only unless a user explicitly approves changes in a source system. <br>


## Reference(s): <br>
- [Matching Rules](references/matching-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/KOwl64/data-reconciliation-exceptions) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, text] <br>
**Output Format:** [Markdown guidance with CSV schemas and exception reason codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only reconciliation guidance; outputs should categorize every record as matched, missing, duplicate, mismatch, or invalid.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
