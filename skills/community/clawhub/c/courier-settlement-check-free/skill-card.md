## Description:

A free deterministic checker for courier outlet settlement sheets that recomputes freight, cash-on-delivery fees, remittance, and payable amounts per row, while flagging understated chargeable weight, duplicate waybills, and missing key fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Courier outlet reconciliation staff, finance teams, and headquarters settlement teams use this skill during monthly settlement review to check freight and cash-on-delivery table arithmetic. It reports row-level findings with source line and waybill references, and it withholds conclusions when required table fields are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean result may be mistaken for complete settlement assurance even though the free version omits listed checks and does not verify contract terms, bank records, tax treatment, or business documents outside the input table.

Mitigation: Review the omitted and out-of-scope checks, verify arithmetic against the original business records, and reconcile contract or payment questions with the authoritative records.

Risk: Incomplete or blank table fields can prevent reliable conclusions.

Mitigation: Provide the exported settlement and cash-on-delivery table text with headers and required columns, and treat missing-input messages as blockers rather than as negative findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/courier-settlement-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Shell commands]

**Output Format:** [Human-readable Chinese text or JSON with findings, summary, executed checks, omitted checks, and input-completeness status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line and waybill when available; insufficient input returns missing-field guidance instead of a clean result.]

## Skill Version(s):

1.0.8 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
