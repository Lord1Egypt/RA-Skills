## Description:

Reconciles data sources using stable identifiers such as Pay Number and driver document numbers, producing exception reports and no-silent-failure checks for weekly matching with explicit reasons for non-joins and mismatches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kowl64](https://clawhub.ai/user/kowl64)

### License/Terms of Use:


## Use Case:

Developers, data analysts, and operations teams use this skill to plan deterministic reconciliation between payroll, compliance, or weekly export datasets and produce exception-report specifications with reason codes, variance checks, and review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive payroll or driver-document data may be exposed if unnecessary fields are used or reports are shared too broadly.

Mitigation: Use only the minimum datasets needed, confirm column mappings and tolerances, and review exception reports before sharing them outside the intended audience.

Risk: Incorrect mappings, competing identifiers, or unspecified tolerances can produce misleading reconciliation results.

Mitigation: Confirm source columns and key priority before matching, use deterministic rules first, and stop for user clarification when mappings or tolerances are missing.

## Reference(s):

- [Matching Rules](references/matching-rules.md)
- [Exceptions Report Template](assets/exceptions-report-template.csv)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with CSV schema snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an exceptions report schema, reason-code taxonomy, normalization rules, join strategy, and tolerance gates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
