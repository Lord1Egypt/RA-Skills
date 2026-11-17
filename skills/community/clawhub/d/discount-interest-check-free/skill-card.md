## Description:

票据贴现计算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号，本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance operations teams use this skill to check bill discount interest worksheets before discounting. It recalculates discount interest, net proceeds, day counts, totals, duplicate bill numbers, and missing fields while citing source line numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Node script over worksheet text supplied by the user.

Mitigation: Review and scan the artifact before installation, run it in a trusted workspace, and provide only the worksheet text needed for the check.

Risk: The output could be mistaken for financial or legal advice or for a complete bill-discounting audit.

Mitigation: Use the output as arithmetic worksheet-checking support only, and confirm discounting terms, market rates, legal issues, and final decisions with the relevant financial or legal reviewers.

Risk: The free version omits several checks, including rate-range, inverted-date, non-positive-face-value, invalid-net-amount, and over-365-day checks.

Mitigation: Review the reported checks-not-run list and verify omitted conditions separately before relying on the worksheet.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/discount-interest-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable text or JSON containing worksheet findings, source line references, summaries, executed checks, and checks not run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally over provided worksheet text; returns insufficient-input guidance instead of conclusions when required columns or rows are missing.]

## Skill Version(s):

1.0.37 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
