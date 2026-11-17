## Description:

建筑企业月度自查包（免费版）核对分包结算与产值、工程进度款与质保金、工程产值与进度确认材料，逐条给出原文依据、可离线复算的检查结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Construction finance staff, cashiers, and operators use this skill during monthly closing or reconciliation to check segmented Chinese construction finance materials for arithmetic consistency, totals, duplicates, blanks, and missing required inputs. It helps reviewers identify issues in supplied tables, but does not replace accounting, legal, audit, tax, valuation, or site-certification judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat reconciliation output as accounting, legal, audit, tax, or certification advice.

Mitigation: Use outputs as arithmetic and reconciliation assistance only, and have qualified reviewers confirm financial, contractual, legal, audit, and tax conclusions before relying on them.

Risk: A clean result can be misread when required sections, headers, or free-version checks are missing.

Mitigation: Review missing-input messages and the listed checks not run; provide only the required materials and do not treat unexecuted checks as passed.

Risk: Sensitive project or finance materials may be included in user inputs.

Mitigation: Provide only the materials needed for the check and avoid unnecessary personal, credential, or confidential data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/construction-monthly-selfcheck-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, analysis, shell commands, guidance]

**Output Format:** [Human-readable terminal text or JSON containing executed checks, findings, missing input notices, source-grounded evidence, and summary counts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with user-provided segmented text input; materials不足时不给结论; free version reports checks not run.]

## Skill Version(s):

1.0.52 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
