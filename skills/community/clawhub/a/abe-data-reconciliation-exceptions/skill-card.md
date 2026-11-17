## Description:

Reconciles data sources using stable identifiers (Pay Number, driving licence, driver card, and driver qualification card numbers), producing exception reports and "no silent failure" checks for weekly matching with explicit reasons for non-joins and mismatches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external reviewers, and data operations teams use this skill to reconcile two CSV/XLSX data sources by stable payroll or driver-document identifiers, categorize every record, and produce exception reporting with quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exception reports may contain payroll numbers, names, and driver document identifiers.

Mitigation: Use the skill only with datasets intended for agent inspection, keep generated reports in an appropriate location, and review anomalies before changing source systems.

Risk: Ambiguous column mappings, competing identifiers, or unspecified tolerances can produce misleading reconciliation results.

Mitigation: Confirm column mappings, identifier priority, and thresholds before reconciliation; stop for user input when mappings or tolerances are ambiguous.

## Reference(s):

- [Matching Rules](references/matching-rules.md)
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/abe-data-reconciliation-exceptions)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with a CSV exception-report schema and reason codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; every record should be categorized or escalated before source data changes.]

## Skill Version(s):

1.0.0 (source: evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
