## Description:

BOM Toolkit helps agents manage bill-of-materials workflows, including completeness checks, version comparison, mechanical/electrical splitting, supplier BOM merging, and change-note generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and transform BOM spreadsheets for non-standard automation projects, especially before procurement, supplier consolidation, or engineering-change review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier BOM workbooks may contain untrusted spreadsheet content, including formula-like values that can carry into generated reports.

Mitigation: Treat supplier workbooks as untrusted, sanitize formula-like cell values before opening generated reports, and review generated workbooks before use.

Risk: Ad hoc dependency installation can introduce supply-chain exposure.

Mitigation: Install dependencies such as openpyxl from a pinned, trusted environment.

Risk: Irregular or ambiguous BOM rows can lead to incorrect classification, comparison, or missing-part conclusions.

Mitigation: Manually review unclassified items, fuzzy matches, and critical findings before procurement or engineering-change decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/bom-toolkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, Python scripts, terminal commands, and Excel workbook reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local BOM spreadsheet files and may generate merged, split, comparison, or change-report Excel files.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
