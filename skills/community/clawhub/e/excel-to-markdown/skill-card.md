## Description: <br>
Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to extract readable Markdown from Word documents, PowerPoint presentations, and Excel spreadsheets provided as local files or URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected office documents or document URLs are uploaded to MinerU cloud processing. <br>
Mitigation: Use only documents the user is authorized to process, and avoid confidential, regulated, or local-only files unless cloud upload is permitted. <br>
Risk: The skill depends on the external mineru-open-api CLI and MinerU service availability. <br>
Mitigation: Install the CLI from the documented package sources and verify the command behavior with non-sensitive files before relying on the output. <br>


## Reference(s): <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The conversion output is Markdown; embedded images may be replaced with placeholders, and flash extraction is limited to 10MB or 20 pages per document.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
