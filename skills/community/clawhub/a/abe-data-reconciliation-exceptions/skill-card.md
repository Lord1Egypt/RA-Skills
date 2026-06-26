## Description: <br>
Reconciles data sources using stable identifiers (Pay Number, driving licence, driver card, and driver qualification card numbers), producing exception reports and no silent failure checks for weekly matching with explicit reasons for non-joins and mismatches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to reconcile two or more CSV/XLSX data sources with stable identifiers, produce an exceptions report, and stop or escalate when mappings, tolerances, duplicates, invalid keys, or unmatched rows are ambiguous. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous column mappings, competing identifiers, or unspecified tolerances can produce misleading reconciliation results. <br>
Mitigation: Stop and ask the user to confirm mappings, key priority, and quality gates before categorizing records. <br>
Risk: Unmatched rows, duplicate keys, or invalid identifiers can be silently dropped if reconciliation output is incomplete. <br>
Mitigation: Always produce an exceptions report with explicit categories and reason codes, and route exceptions to review. <br>
Risk: Source records could be changed accidentally during reconciliation. <br>
Mitigation: Keep source data read-only by default and report exceptions separately unless the user explicitly requests edits. <br>


## Reference(s): <br>
- [Matching Rules](references/matching-rules.md) <br>
- [Exceptions Report Template](assets/exceptions-report-template.csv) <br>
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/abe-data-reconciliation-exceptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with CSV exception-report schema and reason codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference a standardized CSV template and matching-rules reference; source data should remain read-only unless the user explicitly requests changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
