## Description:

Supports Chinese-language food R&D document classification, version tracking, template generation, and document drafting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudyxuq](https://clawhub.ai/user/cloudyxuq)

### License/Terms of Use:

MIT-0

## Use Case:

Food R&D teams and document authors use this skill to organize research materials, classify documents by lifecycle and document type, manage versions, and draft reports or process records from templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps a local document index under data/docs, which may include project document metadata.

Mitigation: Review local index contents before sharing the workspace and avoid storing confidential details unless the workspace is approved for that data.

Risk: The skill suggests generic web searches for document standards, which can disclose query text to external search providers.

Mitigation: Keep web-search queries generic and remove confidential project, product, or customer details before searching.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudyxuq/skills/food-document-management)
- [R&D document classification standard](artifact/references/document_classification.md)
- [Document template index](artifact/assets/templates/README.md)
- [Small-scale trial report template](artifact/assets/templates/trial_report.md)
- [Process record template](artifact/assets/templates/process_record.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown templates, text guidance, shell command suggestions, Python helper code, and JSON document index entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local files under data/docs when the document-management helper script is used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
