## Description:

Generates structured Excel test cases from requirements documents, API specifications, and project documentation, with support for embedded image and flowchart analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thanksjj](https://clawhub.ai/user/thanksjj)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, developers, and product teams use this skill to turn PDF, Word, Markdown, API, and project documentation into traceable test cases, analysis briefs, and validation reports. It is intended for structured test-design workflows that need scope confirmation, path coverage, seven-dimension coverage, and reviewable Excel output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated test cases or validation reports may be incomplete or misleading when requirements are ambiguous or visual content is misread.

Mitigation: Review the generated test cases and validation report against the source requirements before relying on them for release decisions.

Risk: Dependency installation and helper-script execution can vary across local environments.

Mitigation: Install dependencies in an isolated virtual environment and prefer pinned package versions.

Risk: The workflow and templates are primarily Chinese-language, so non-Chinese deliverables may need extra scrutiny.

Mitigation: Review non-Chinese output for terminology, coverage, and formatting before delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thanksjj/skills/auto-testcase-generator)
- [Requirements Analysis Brief Template](references/analysis_template.md)
- [Excel Output Format Specification](references/excel_format.md)
- [Image Processing and Flowchart Analysis](references/image_processing.md)
- [PDF Image Extraction Script](scripts/extract_pdf_images.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown reports, Mermaid diagrams, Excel workbook output, and Python or shell guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Excel output is specified as a single worksheet grouped by module with 12 standard columns, traceability fields, priority labels, and validation summaries.]

## Skill Version(s):

1.1.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
