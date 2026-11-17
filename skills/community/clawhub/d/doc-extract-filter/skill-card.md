## Description:

Extracts text from PDF, Word, Excel, text, CSV, Markdown, and WPS documents and filters content with keywords, regular expressions, exclusions, context windows, and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigclawd](https://clawhub.ai/user/bigclawd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing agents use this tool to extract text from common office and document formats, search for relevant passages with keyword or regex filters, and process individual files or batches into structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch processing can read broad local folders and write extracted document text into JSON output files.

Mitigation: Run batch mode only on intended folders, choose the output directory deliberately, and protect or delete generated JSON files when they contain sensitive content.

Risk: Untrusted PDFs and complex regular expressions can be resource-intensive, especially when OCR is enabled.

Mitigation: Install in a virtual environment, review or pin dependencies, limit input size, validate regex patterns, and enable OCR only when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigclawd/skills/doc-extract-filter)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [JSON objects containing extracted text, filtered matches, match counts, error fields, and optional batch result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch mode can write per-file JSON result files or one merged JSON file.]

## Skill Version(s):

1.1.1 (source: server release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
