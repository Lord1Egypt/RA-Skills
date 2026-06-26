## Description: <br>
Create, read, edit, and manipulate Word documents (.docx). Supports text, tables, images, headers, footers, styles, and tracked changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weaglewang](https://clawhub.ai/user/weaglewang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, read, edit, validate, and convert Microsoft Word .docx documents, including reports, invoices, resumes, tables, images, headers, footers, and document XML edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install several third-party document tools. <br>
Mitigation: Install only the tools needed for the current task from trusted package managers, and prefer pinned or project-local dependencies where practical. <br>
Risk: Document and image processing may expose content the user did not intend the agent to read or modify. <br>
Mitigation: Use the skill only with documents and images that are intended for agent review or modification. <br>
Risk: Manual XML edits or generated document structures can produce invalid or incorrectly rendered .docx files. <br>
Mitigation: Keep an original copy and validate generated files with python-docx, pandoc, or the documented validation workflow before distribution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/weaglewang/docx-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/weaglewang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and Python code examples, shell commands, and document-processing checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to install and use docx, pandoc, python-docx, LibreOffice, and ImageMagick; generated documents should be validated before distribution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
