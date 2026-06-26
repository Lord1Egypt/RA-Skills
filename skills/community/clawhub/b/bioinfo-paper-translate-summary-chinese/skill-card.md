## Description: <br>
Extracts text from an English research paper PDF, then prompts the agent to translate and summarize it in Chinese with emphasis on bioinformatics details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zd200572](https://clawhub.ai/user/zd200572) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and technical readers use this skill to turn an English PDF paper into Chinese reading notes and summaries tailored to bioinformatics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The full extracted PDF text is sent into the agent conversation. <br>
Mitigation: Use the skill only with papers whose contents are appropriate to share with the configured agent and workspace. <br>
Risk: The skill writes a temporary file named temp_paper_for_translation.txt next to the input PDF. <br>
Mitigation: Run it in a directory where that filename is not used for important content. <br>
Risk: PDF text extraction depends on the local pdftotext binary. <br>
Mitigation: Install poppler-utils from a trusted package source and expect lower quality on scanned or complex PDFs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zd200572/bioinfo-paper-translate-summary-chinese) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text prompt containing extracted paper text and instructions to produce Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an absolute PDF path and the pdftotext command from poppler-utils.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
