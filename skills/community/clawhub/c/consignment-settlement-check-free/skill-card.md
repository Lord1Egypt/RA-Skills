## Description:

寄售代销结算台账逐行复算，核对寄售结存、应结金额、代销手续费、发货数量、合计行、重复清单号、空缺、负值和日期倒挂，并为每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Retail, manufacturing, and brand finance or operations teams use this skill during monthly consignment settlement review to recompute ledger rows and identify arithmetic or consistency issues before settlement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free release performs arithmetic and consistency checks but does not perform the listed full-tier checks such as sold-but-unsettled detection or contract-rate overcharge detection.

Mitigation: Confirm whether the free-tier scope is sufficient for the settlement decision; use the full workflow or manual review for omitted checks.

Risk: The skill does not provide legal, tax, invoice, or contract advice.

Mitigation: Route contract validity, tax treatment, invoice reconciliation, and collection decisions to the appropriate finance, tax, or legal reviewer.

Risk: Missing or unrecognized ledger material can prevent reliable conclusions.

Mitigation: Provide consignment ledger text with complete headers and source rows, and treat insufficient-input output as no conclusion rather than as a pass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/consignment-settlement-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text or JSON findings with source row references and summary fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-supplied consignment ledger text; reports insufficient input instead of drawing conclusions when required ledger material is missing.]

## Skill Version(s):

1.0.54 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
