## Description:

Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. Use when extracting content from Word documents, PowerPoint presentations, or Excel spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract content from Word, PowerPoint, and Excel files into Markdown for reading, summarization, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads documents to MinerU's cloud API for processing.

Mitigation: Avoid sending confidential or regulated documents unless MinerU's privacy terms satisfy the user's requirements.

Risk: The skill depends on an external CLI installed through npm, uv, or go, and package versions are not pinned in the release metadata.

Mitigation: Install and run the CLI in a low-privilege or sandboxed environment and review the resolved package before use.

Risk: The flash-extract path is documented for documents up to 10MB or 20 pages, and embedded images may be replaced with placeholders.

Mitigation: Use the authenticated MinerU extract workflow for larger or precision-sensitive documents, and verify extracted Markdown against the source file.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tanis90/skills/docx-to-markdown)
- [Publisher Profile](https://clawhub.ai/user/tanis90)
- [MinerU](https://mineru.net)
- [MinerU CLI Download](https://mineru.net/ecosystem?tab=cli)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown content with CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MinerU Open API for document extraction; flash-extract is documented for files up to 10MB or 20 pages, and embedded images may be replaced with placeholders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
