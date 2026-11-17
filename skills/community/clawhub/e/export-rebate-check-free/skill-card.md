## Description:

This Chinese-language skill locally checks export VAT rebate worksheets by recalculating disclosed formulas, totals, duplicates, and blank fields, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking finance, tax, and operations users at export businesses use this skill before monthly export VAT rebate filing to check worksheet arithmetic, row totals, duplicate declaration numbers, and missing key fields. It supports local deterministic review but does not decide legal rebate rates or eligibility.

### Deployment Geography for Use:

Global, for users handling Chinese export VAT rebate worksheets

## Known Risks and Mitigations:

Risk: The skill does not validate legally correct rebate rates, tax eligibility conditions, or the checks explicitly omitted from the free version.

Mitigation: Treat results as worksheet arithmetic and consistency checks only, and confirm rebate rates, eligibility, and omitted checks through authoritative tax review.

Risk: Broad trigger wording may cause the skill to appear during general discussions of rebate rates.

Mitigation: Use it only when the user needs Chinese export VAT rebate worksheet checking, and confirm the task scope before running the checker.

Risk: The checker reads user-provided worksheet content from local files.

Mitigation: Provide only the worksheet content needed for the check and avoid including unrelated confidential material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/export-rebate-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Sample worksheet input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown usage guidance plus terminal text or JSON results from local Node commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers and include executed checks, omitted checks, summary totals, and insufficient-input guidance.]

## Skill Version(s):

1.0.36 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
