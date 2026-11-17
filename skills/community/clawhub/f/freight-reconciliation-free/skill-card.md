## Description:

Checks freight monthly statements for row-level arithmetic, totals, duplicate waybills, and missing values, with each finding tied to the source line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and warehouse teams use this skill during monthly freight reconciliation to check whether a carrier statement's arithmetic, totals, duplicate waybills, and required numeric fields are internally consistent. It is an arithmetic reconciliation aid, not a logistics pricing, tax, audit, shipment, or supplier-management review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Node.js script on freight statement material.

Mitigation: Install and run it only in an environment where local processing of business documents is acceptable.

Risk: A clean result may be mistaken for a full audit, shipment validation, or logistics-price validation.

Mitigation: Treat the output as internal arithmetic reconciliation only, and review the listed withheld and out-of-scope checks before relying on results.

Risk: The free version intentionally omits several checks available outside this package.

Mitigation: Review the reported checks_given, checks_withheld, and checks_out_of_scope fields before deciding whether the result is sufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/freight-reconciliation-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON from a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source lines; insufficient input returns missing-material guidance instead of a clean conclusion.]

## Skill Version(s):

1.1.30 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
