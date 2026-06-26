## Description: <br>
Analyzes and organizes PDFs in a local folder by extracting text, classifying documents by topic, moving PDFs into topic folders, and generating a structured report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyj0124](https://clawhub.ai/user/wyj0124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and knowledge workers use this skill to batch-process PDFs in a local folder, classify them by topic, organize the original files into category folders, and produce a consolidated report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read every PDF in the chosen folder and save full extracted document text into that folder. <br>
Mitigation: Use it only on folders approved for agent access, and review where extracted text files will be stored before execution. <br>
Risk: The skill can automatically move PDFs into newly created category folders without a required preview. <br>
Mitigation: Run it on a copy of important folders first, request a dry-run plan, and require explicit confirmation before file moves. <br>


## Reference(s): <br>
- [Default report template](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with supporting extracted text JSON and local file organization actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write extracted document text into the selected folder and move PDFs into generated topic folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
