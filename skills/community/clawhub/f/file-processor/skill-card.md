## Description: <br>
Automatically detects and processes PDF, Excel, CSV, Word, image, and text files for extraction, OCR, data preview, and summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ly5201314gjx](https://clawhub.ai/user/ly5201314gjx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect common user-provided files, extract readable text or tabular previews, run OCR on images, and summarize long document content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided files may contain secrets, regulated data, or confidential document content that can appear in extracted text, OCR output, chat transcripts, or logs. <br>
Mitigation: Use the skill only with files the user intends the agent to read, and avoid processing sensitive documents unless that exposure is acceptable. <br>
Risk: The skill depends on external Python packages and a local OCR engine, so unavailable or untrusted dependencies can cause failures or supply-chain risk. <br>
Mitigation: Install dependencies from trusted package sources in a virtual environment and verify the local Tesseract OCR installation before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown-style text with extracted previews, status messages, and dependency installation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local file-processing summaries and previews; long content is truncated before display.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
