## Description:

Parse, analyze, and extract content from documents (PDF, DOCX, PPTX, audio). Supports OCR, table extraction, and semantic chunking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c7934597](https://clawhub.ai/user/c7934597)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to process PDFs, DOCX files, PPTX decks, and audio files, then extract, summarize, translate, or answer questions about the resulting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document contents may be handled by Akashic MCP services during processing.

Mitigation: Use the skill only for explicit document-analysis tasks, and avoid sensitive files unless sharing them with the configured processing service is approved.

Risk: Broad activation phrases may match general file or document requests.

Mitigation: Invoke the skill only when the user clearly requests analysis, extraction, summarization, transcription, or translation of a supported document or audio file.

Risk: OCR or transcription quality can be poor for low-resolution scans or unclear audio.

Mitigation: Ask for a higher-quality source when quality is poor and clearly qualify uncertain extracted content.

## Reference(s):

- [Akashic Doc Analyzer on ClawHub](https://clawhub.ai/c7934597/skills/akashic-doc-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text summaries, extracted content, translations, and answers based on processed documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference document chunks, OCR results, extracted tables, slide content, or audio transcript segments returned by Akashic MCP tools.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
