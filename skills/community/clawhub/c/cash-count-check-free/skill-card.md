## Description:

现金盘点表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。触发词包括 现金盘点、长短款、收银对账、备用金。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators, finance teams, and reviewers use this skill to check cash-count tables for arithmetic consistency, total-row issues, duplicate store-shift rows, blanks, and difference-sign/type mismatches. It is intended as a local table consistency check, not as an audit, legal, or fraud determination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cash-count consistency findings may be mistaken for audit, legal, or fraud conclusions.

Mitigation: Treat outputs as arithmetic and table-consistency checks only; have qualified reviewers investigate causes and compliance implications.

Risk: The free version omits documented checks such as threshold exceedance, negative cash values, and some value-legality checks.

Mitigation: Review the listed withheld checks before relying on the result, and run additional controls when those checks matter.

Risk: Incorrect or incomplete table headers can prevent reliable checking.

Mitigation: Provide the expected cash-count table headers and review missing-input messages before drawing any conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cash-count-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON from local Node execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input reports missing fields without issuing a conclusion.]

## Skill Version(s):

1.0.57 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
