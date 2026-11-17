## Description:

加盟结算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Franchise operations, finance, and settlement reviewers use this skill to check Chinese-language franchise royalty worksheets for recomputed royalty amounts, ad-fund amounts, payable totals, totals rows, duplicate franchisees, and blank or placeholder fields. It is intended as a local worksheet checker and not as contract, legal, or tax advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can produce misleading confidence if users treat a passed worksheet check as contract, legal, tax, or revenue-recognition approval.

Mitigation: Use the output only to verify the arithmetic and table consistency checks that the skill says it executed; separately review contract terms, tax treatment, and revenue definitions.

Risk: The free version explicitly withholds several range and negative-value checks, so unusual rates or negative values may require additional review.

Mitigation: Review the listed withheld checks before relying on results, and run additional validation when rate bounds, non-positive revenue, or negative guarantee/payable values matter.

Risk: Material with missing headers or insufficient rows cannot be checked and should not be interpreted as having no findings.

Mitigation: Provide a complete settlement table with recognizable headers and at least one franchisee detail row; when the tool reports insufficient input, correct the input before drawing conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/franchise-royalty-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON containing findings, summary totals, executed checks, withheld checks, line references, and guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; accepts a JSON or plain-text franchise settlement table and does not use network access.]

## Skill Version(s):

1.0.32 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
