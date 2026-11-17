## Description:

Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. Use when extracting content from Word documents, PowerPoint presentations, or Excel spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to extract content from Word, PowerPoint, and Excel documents into Markdown for reading, summarization, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supported Office documents are uploaded to MinerU's cloud processing service during flash extraction.

Mitigation: Avoid sensitive, regulated, or confidential files unless MinerU's terms and data handling are acceptable for the use case.

Risk: The skill depends on installing and executing the third-party mineru-open-api CLI.

Mitigation: Install from a trusted package source and prefer a sandboxed environment for installation and conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanis90/skills/excel-to-markdown)
- [MinerU](https://mineru.net)
- [MinerU CLI download](https://mineru.net/ecosystem?tab=cli)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converts supported Office documents from local files or URLs; normal flash extraction is limited to 10MB or 20 pages per document.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
