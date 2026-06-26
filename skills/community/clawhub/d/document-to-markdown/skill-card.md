## Description: <br>
Converts DOCX, PPTX, XLS, and XLSX files to Markdown using MinerU Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to extract Markdown from Word documents, PowerPoint presentations, Excel spreadsheets, or document URLs for summarization, analysis, and downstream editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to MinerU's cloud service for processing. <br>
Mitigation: Avoid confidential, regulated, customer, or internal business documents unless policy allows third-party cloud processing. <br>
Risk: Large or precision-sensitive documents may exceed the flash extraction limits. <br>
Mitigation: Use the authenticated mineru-open-api extract workflow for larger files or precision extraction when that processing path is approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tanis90/document-to-markdown) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI download](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the mineru-open-api CLI; flash extraction is limited to 10 MB or 20 pages per document, and embedded images may be replaced with placeholders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
