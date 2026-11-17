## Description:

承运司机运费结算单逐项核对（运费复算、逐单应付运费复算、对账单合计勾稽、重复运单与空缺检测），每条结论引用原文行号与运单号。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, dispatch, and settlement staff at logistics companies, fleet operators, and route carriers use this skill to locally check driver freight settlement sheets before payment. It recomputes freight and payable amounts, reconciles statement totals, and reports differences with source line and waybill references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean result could be mistaken for approval to pay even though the skill does not verify contracts, external TMS records, oil-card records, or legal validity of deductions.

Mitigation: Treat findings as settlement-sheet checks only and require business review against contracts, source systems, and deduction evidence before releasing payment.

Risk: The free version omits higher-level checks such as receipt-missing decisions, unsupported deduction disputes, duplicate oil-card charging, rate-tier validation, and driver-level pre-payment action lists.

Mitigation: Confirm whether omitted checks are needed for the settlement workflow and perform them separately before relying on the result.

Risk: Inputs without required columns or recognizable settlement fields do not support a conclusion.

Mitigation: Provide a headered settlement table with the required freight, deduction, advance toll, and payable fields; treat insufficient-input responses as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/driver-freight-settlement-check-free)
- [Server-resolved provenance unavailable](No server-resolved GitHub import provenance is stored for this version.)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis, Guidance]

**Output Format:** [Plain text or JSON freight settlement findings with source line and waybill references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against user-provided settlement text; reports insufficient input instead of issuing unsupported conclusions.]

## Skill Version(s):

1.0.50 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
