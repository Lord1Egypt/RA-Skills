## Description:

Generate import-ready data from user-provided Excel or CSV templates based on the customer's described business scenario.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huahuaweiwei](https://clawhub.ai/user/huahuaweiwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect uploaded spreadsheet import templates and generate synthetic rows that preserve the target sheet, headers, column order, and apparent field formats. It is intended for sample, test, or initialization data generation from a user-described business scenario.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated rows or inferred field mappings may not match strict import validation rules.

Mitigation: Review the chosen sheet, headers, assumptions, and generated data before importing into a real system.

Risk: Large or untrusted spreadsheet templates can add processing risk or produce misleading structure detection.

Mitigation: Use reasonably sized templates from trusted sources and inspect ambiguous sheets or required dictionaries before generation.

Risk: Non-Chinese or non-English templates may reduce mapping accuracy.

Mitigation: Check inferred column meanings and provide missing business context or code mappings when labels are ambiguous.

## Reference(s):

- [Generation Guidelines](artifact/references/generation-guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, shell commands, guidance]

**Output Format:** [Markdown summaries with tables or fenced CSV, plus optional generated spreadsheet files when working in a workspace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [States the chosen sheet, detected headers, row count, and material assumptions before import use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
