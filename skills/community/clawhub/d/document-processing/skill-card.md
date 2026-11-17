## Description:

Processes documents by converting common office formats, extracting text, tables, images, and OCR text, and supporting batch workflows with optional Feishu synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongrui-xr](https://clawhub.ai/user/xiongrui-xr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-automation agents use this skill to convert documents, extract structured content, run batch processing, and optionally push processed results to Feishu cloud documents or tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document contents may be synchronized to Feishu without clear data-transfer boundaries.

Mitigation: Use Feishu synchronization only when upload is explicit, and avoid processing sensitive documents through that workflow unless approved.

Risk: Batch processing uses a default temporary directory that may be unsuitable on shared systems.

Mitigation: Configure a private temporary directory with appropriate access controls before running batch conversions.

Risk: Generated CSV files from untrusted spreadsheets may carry formula-related risks when opened in spreadsheet tools.

Mitigation: Sanitize or escape formula-like cell values before sharing or opening generated CSV files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xiongrui-xr/skills/document-processing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, shell, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce converted document files, extracted content, CSV files, and Feishu synchronization guidance depending on the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
