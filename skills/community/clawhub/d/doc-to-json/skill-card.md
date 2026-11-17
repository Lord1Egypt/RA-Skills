## Description:

Converts DOC, DOCX, PDF, XLSX, and XLS files into structured JSON using MinerU extraction and a Markdown-to-JSON parser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kounlong](https://clawhub.ai/user/kounlong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to convert office documents and PDFs into structured JSON for RAG preparation, metadata extraction, and course, standards, or report processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents processed by the full pipeline may be sent through MinerU.

Mitigation: Use the skill only with files that are acceptable to process through MinerU, and verify MinerU's data-handling terms before use.

Risk: The MinerU token is passed through process arguments by the included script.

Mitigation: Prefer a safer supported token mechanism before deployment, especially on shared systems where process arguments may be visible.

Risk: Converted JSON may be used downstream for RAG or database preparation.

Mitigation: Review the generated JSON structure and extracted metadata before indexing, embedding, or importing it into another system.

## Reference(s):

- [KB Preparation Patterns](references/kb-prep.md)

## Skill Output:

**Output Type(s):** [json, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mineru-open-api v0.5+ and a MINERU_TOKEN environment variable for the full document extraction pipeline.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
