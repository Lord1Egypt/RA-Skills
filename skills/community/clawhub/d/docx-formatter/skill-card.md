## Description: <br>
DOCX Formatter generates Chinese official-document .docx files with prescribed title, heading, body, page, and punctuation formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rokami](https://clawhub.ai/user/Rokami) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and document-preparation agents use this skill to create formal Chinese Word documents from Markdown or structured JSON while applying official-document typography and layout conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The python-docx dependency is unpinned, which can reduce reproducibility across installations. <br>
Mitigation: Review and pin dependency versions before controlled or repeatable deployments. <br>
Risk: The formatter writes .docx files to caller-selected output paths, which can overwrite existing files. <br>
Mitigation: Choose output paths deliberately and review generated files before sharing or replacing documents. <br>


## Reference(s): <br>
- [ClawHub DOCX Formatter listing](https://clawhub.ai/Rokami/docx-formatter) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [DOCX files generated from Markdown or JSON, with Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes caller-selected .docx output paths; final typography depends on availability of the named Chinese fonts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
