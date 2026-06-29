## Description: <br>
Converts PDF, DOCX, XLSX, PPTX, HTML, CSV, and other local files to Markdown using the @covoyage/file2md CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luduoxin](https://clawhub.ai/user/luduoxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert local documents, spreadsheets, presentations, HTML, CSV, notebooks, archives, email, and supported media files into readable Markdown. It is intended for local file or stdin conversion, with optional cloud processing only when Azure use is approved for the data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Azure Document Intelligence or Azure Content Understanding modes can send document contents to Azure services. <br>
Mitigation: Confirm files are permitted to be processed by Azure and avoid cloud modes for sensitive documents unless explicitly approved. <br>


## Reference(s): <br>
- [ClawHub File2md Skill](https://clawhub.ai/luduoxin/skills/file2md) <br>
- [@covoyage/file2md npm package](https://www.npmjs.com/package/@covoyage/file2md) <br>
- [file2md repository](https://github.com/covoyage/file2md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write converted Markdown to stdout or to a file with -o; large conversions should use an output file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
