## Description: <br>
Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other users use this skill to extract readable Markdown from Word, PowerPoint, and Excel documents so the content can be reviewed, summarized, or analyzed by an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected Office documents are uploaded to MinerU's external cloud API for processing. <br>
Mitigation: Use only with documents appropriate for that service; avoid confidential, regulated, or highly sensitive files unless the user explicitly trusts MinerU's handling of uploaded content. <br>
Risk: The documented quick path supports a maximum of 10MB or 20 pages per document. <br>
Mitigation: Use the authenticated mineru-open-api extract workflow for larger or precision extraction needs, or choose another conversion path when the file exceeds those limits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tanis90/docx-to-markdown) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI Download](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mineru-open-api flash-extract; output is Markdown and embedded images may be replaced with placeholders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
