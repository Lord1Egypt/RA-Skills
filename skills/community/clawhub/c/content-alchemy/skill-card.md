## Description: <br>
Turn articles, web pages, PDFs, and excerpts into structured notes, key insights, practical actions, and reusable takeaways. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inf-lucas](https://clawhub.ai/user/inf-lucas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use Content Alchemy to convert text, web pages, and PDFs into saved reading outcomes, including structured notes, insights, actions, and reusable takeaways. For long PDFs, it supports segmented reading, checkpoints, and resuming progress across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching user-provided URLs can expose requested URLs to remote sites and may fail on dynamic or low-quality pages. <br>
Mitigation: Fetch only URLs the user provides, avoid --insecure except for deliberate TLS troubleshooting, and ask for source text when extraction is weak. <br>
Risk: Long-PDF progress, notes, and checkpoints are saved locally in plaintext under ~/.content-alchemy/sessions. <br>
Mitigation: Process sensitive documents only when local plaintext storage is acceptable, and delete saved session files when they are no longer needed. <br>
Risk: PDF processing depends on local pdftotext/pdfinfo tools and does not include OCR for scanned PDFs. <br>
Mitigation: Verify extracted text quality and recommend OCR or source text when the PDF appears scanned or text extraction is sparse. <br>


## Reference(s): <br>
- [Content Alchemy ClawHub Page](https://clawhub.ai/inf-lucas/content-alchemy) <br>
- [README](README.md) <br>
- [Content Alchemy Feature Guide](docs/FEATURE_GUIDE.md) <br>
- [ClawHub Release Notes](docs/CLAWHUB_RELEASE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown notes and checkpoint summaries, with shell commands for web/PDF extraction and session management] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Long-PDF reading plans, state files, segment results, and checkpoint summaries may be saved locally under ~/.content-alchemy/sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
