## Description:

A local factory-overhead allocation and absorption checker that recomputes allocation rates, allocated amounts, allocation totals, absorption rates, duplicate rows, and missing required fields, with source row references for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Cost accountants, workshop accounting staff, and finance supervisors use this skill during month-end closing, cost accounting, and operating analysis to check factory overhead collection and allocation tables before product-cost carry-forward. It is intended for pasted or exported table text, and it reports insufficient input instead of issuing unsupported conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide unrelated sensitive documents even though the checker is designed for factory-overhead allocation table text.

Mitigation: Provide only the relevant exported or pasted allocation table fields needed for the check, and avoid unrelated sensitive documents.

Risk: The free version omits several advanced checks, including cross-workshop or cross-period ledger reconciliation, absorption variance threshold handling, and three-factor variance attribution.

Mitigation: Review the reported checks_not_run and checks_out_of_scope before relying on the result for month-end close or audit preparation.

Risk: The checker validates arithmetic consistency inside the provided table but does not judge whether allocation bases, source records, or accounting policy choices are correct.

Mitigation: Validate allocation bases and accounting policy decisions against the organization's cost-accounting procedures and source systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/factory-overhead-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable CLI text or machine-readable JSON containing status, findings, summary, scope, missing inputs, and advice.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source row numbers and formulas; insufficient input produces missing-field guidance instead of findings.]

## Skill Version(s):

1.0.5 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
