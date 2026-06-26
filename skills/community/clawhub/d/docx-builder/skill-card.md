## Description: <br>
Docx Builder helps agents produce runnable Node.js scripts that generate styled Word .docx documents for PRDs, technical plans, project reports, and meeting notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperkwok](https://clawhub.ai/user/casperkwok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-producing teams use this skill to turn structured document requests into Node.js docx scripts and generated .docx files with consistent headings, tables, colors, and sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scripts may create or overwrite files at user-specified output paths. <br>
Mitigation: Review generated scripts before running them and confirm filenames and output paths. <br>
Risk: The skill depends on the docx npm package and local Node.js execution. <br>
Mitigation: Install dependencies from trusted package sources and run generated scripts in an appropriate working directory. <br>


## Reference(s): <br>
- [Docx Builder on ClawHub](https://clawhub.ai/casperkwok/docx-builder) <br>
- [Publisher profile: casperkwok](https://clawhub.ai/user/casperkwok) <br>
- [Project homepage](https://github.com/openclaw/clawhub) <br>
- [docx-template.js](references/docx-template.js) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown with JavaScript code blocks and generated .docx file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, and the docx npm package.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
