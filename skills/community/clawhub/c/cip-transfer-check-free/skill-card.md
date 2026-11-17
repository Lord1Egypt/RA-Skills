## Description:

在建工程转固台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during monthly close, reconciliation, or inventory checks to review CIP-to-fixed-asset transfer ledgers. It recalculates supported table relationships, checks totals, duplicates, blanks, placeholders, and negative amounts, and cites source lines for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free checker as a complete accounting review even though several checks are explicitly not included.

Mitigation: Review the listed checks_not_run and perform manual or separate paid/full-scope review for date-order checks, transfer amount exceeding CIP cost, difference-rate thresholds, and post-transfer CIP activity.

Risk: Insufficient or unrecognized ledger input produces no accounting conclusion.

Mitigation: Provide the required CIP transfer ledger columns with usable headers and do not interpret insufficient-input output as no issue found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cip-transfer-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console output or JSON findings with cited source lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; no network, registration, API key, persistence, credential access, or data mutation is reported in security evidence.]

## Skill Version(s):

1.0.50 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
