## Description:

车辆油耗与运费台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and fleet operations staff use this skill during monthly closing or reconciliation to check Chinese-language vehicle fuel and freight ledgers. It recalculates row arithmetic, verifies totals, detects duplicate month/plate entries, flags blanks or placeholders, and reports only findings supported by source text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readers may treat the free-version output as a complete fleet audit even though several checks are intentionally withheld.

Mitigation: Present results as arithmetic review only, and separately review cost-versus-revenue, recharge-versus-fuel, zero-mileage fuel use, and reference-range checks when those questions matter.

Risk: An inconsistent output disclaimer can overstate a check that the free version does not run.

Mitigation: Use the declared free-check list as authoritative for this release and verify any withheld checks with another process or the complete version before relying on them.

Risk: Fuel discrepancies could be misread as proof of misconduct or liability.

Mitigation: Use findings as source-cited reconciliation leads, then confirm against underlying fleet records, contracts, and human review before assigning responsibility.

Risk: Incomplete or malformed ledger input can lead to no executable check.

Mitigation: Provide ledger text with the required headers and source rows; when the skill reports missing input, correct the source material rather than treating the run as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/fleet-fuel-cost-check-free)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable findings or JSON with cited source lines, plus local command examples for running the checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally without network access; insufficient input returns missing requirements rather than a positive or negative audit conclusion.]

## Skill Version(s):

1.0.55 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
