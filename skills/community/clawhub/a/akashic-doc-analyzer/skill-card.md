## Description: <br>
Parse, analyze, and extract content from documents (PDF, DOCX, PPTX, audio). Supports OCR, table extraction, and semantic chunking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c7934597](https://clawhub.ai/user/c7934597) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process user-selected documents, extract structured content, summarize key points, answer questions about the extracted material, and translate content when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-selected documents are processed through an external Akashic MCP service. <br>
Mitigation: Install only if the Akashic MCP provider is trusted for the documents being analyzed; avoid confidential, regulated, or highly personal files unless handling, retention, and access controls have been confirmed. <br>
Risk: OCR, transcription, or extraction quality may be poor for low-resolution scans or difficult audio. <br>
Mitigation: Review extracted content before relying on summaries or answers, and provide a higher-resolution scan or clearer source file when quality is poor. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries, extracted-content sections, answers, translations, and transcription notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Akashic MCP service for document processing, chat completion, and translation.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
