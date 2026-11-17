## Description:

薪酬社保与人力专家 covers 21 payroll, social insurance, housing fund, and HR spreadsheet checks, routes pasted tabular input to the matching check, and returns row-level, reproducible conclusions or missing-column feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external operators in payroll, finance, HR, and compliance-adjacent roles use this skill to run deterministic checks over pasted payroll and HR tables before payment, filing, or reconciliation. It helps identify arithmetic mismatches, missing required columns, unmatched task types, and checks that were not executed because required inputs were absent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive payroll and employee-related data.

Mitigation: Use local processing only with data that the operator is authorized to paste, and avoid real employee identifiers unless local handling is acceptable.

Risk: A persistent local trial counter and paywall behavior may affect execution after repeated use.

Mitigation: Review the local usage counter behavior before deployment and communicate it to users who expect unrestricted local execution.

Risk: Spreadsheet checks can be mistaken for legal, tax, payroll, or HR compliance advice.

Mitigation: Treat outputs as deterministic spreadsheet findings and route compliance-sensitive decisions through qualified human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-payroll-pub)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text status messages and check results, with optional structured JSON for the selected sub-skill result.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally from tabular text or JSON input; results should be treated as spreadsheet checks rather than legal, tax, payroll, or HR compliance advice.]

## Skill Version(s):

1.0.10 (source: server release evidence; artifact frontmatter reports 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
