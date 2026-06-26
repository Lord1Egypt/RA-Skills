## Description: <br>
Processes PDF documents locally for text extraction, summaries, table extraction, keyword-based questions, page splitting, and OCR for scanned Chinese or English PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect local PDF files, extract text and tables, summarize content, split pages, answer keyword-based questions, and OCR scanned documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes local PDF contents and can write split PDFs or OCR text to a user-specified or default local path. <br>
Mitigation: Use it only with documents intended for local processing and review output paths before handling sensitive files. <br>
Risk: Summaries, keyword answers, and OCR output may be incomplete or inaccurate for complex layouts, scanned pages, or low-quality source files. <br>
Mitigation: Review extracted text and generated files against the original PDF before relying on the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-pdf-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, JSON] <br>
**Output Format:** [Markdown or terminal text with optional JSON status and generated PDF or TXT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write split PDF files or OCR text results to a local output path.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
