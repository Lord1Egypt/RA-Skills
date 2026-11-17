## Description:

外币结算核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations users with foreign-currency settlement worksheets use this skill to recalculate settlement rows, totals, duplicate document numbers, blank fields, and FX gain or loss direction from pasted table text. The output cites source line numbers and withholds conclusions when required worksheet fields are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean worksheet result could be mistaken for accounting, tax, or policy validation.

Mitigation: Use the skill as a deterministic consistency checker only; have qualified finance or tax reviewers decide accounting policy, tax treatment, and final conclusions.

Risk: The free release omits specific checks such as non-positive rates, non-positive foreign amounts, large FX movement checks, and negative received-base-amount checks.

Mitigation: Review the reported withheld checks before relying on the output, and perform omitted controls separately when they matter to the settlement review.

Risk: Chinese-oriented header matching and text-table input can fail or miss needed fields when worksheet labels or formats differ.

Mitigation: Provide a table with recognizable headers and review any insufficient-input response instead of treating missing output as confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/fx-settlement-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill source manifest](artifact/SKILL.md)
- [Sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON results with line-cited findings, check lists, withheld checks, and insufficiency messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library scripts; accepts pasted worksheet text or JSON containing text/content.]

## Skill Version(s):

1.0.33 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
