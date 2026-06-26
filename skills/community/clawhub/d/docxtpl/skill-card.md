## Description: <br>
Docxtpl helps agents generate Word (.docx) documents from Microsoft Word templates populated with Python data through docxtpl, python-docx, and Jinja2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to create .docx reports, letters, and batch documents from Jinja2-enabled Word templates and structured data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The batch renderer can write generated files outside the chosen output folder when CSV id values contain path-like text. <br>
Mitigation: Use trusted CSV data, avoid path-like id values, avoid --overwrite with untrusted data, and run batch rendering in a contained working directory until filenames are sanitized. <br>


## Reference(s): <br>
- [Official docxtpl documentation](https://docxtpl.readthedocs.io/en/latest/) <br>
- [Bundled docxtpl reference](references/official-docs.md) <br>
- [ClawHub Docxtpl release](https://clawhub.ai/killgfat/docxtpl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide rendering from inline values, JSON, JSON files, and CSV batch inputs.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
