## Description: <br>
Docx Cn 1.0.1 helps agents create, read, edit, validate, and convert Word .docx documents, including formatting, tables, images, tracked changes, and comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binbin](https://clawhub.ai/user/binbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to inspect, generate, convert, and edit Microsoft Word files while preserving OOXML structure and validating the resulting documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run LibreOffice, create or edit document files, and write a LibreOffice macro profile under /tmp. <br>
Mitigation: Run the skill in an isolated workspace and review document outputs before sharing or using them in production workflows. <br>
Risk: In some sandboxed environments, the skill can compile and preload a native helper shim for LibreOffice. <br>
Mitigation: Review or replace the LD_PRELOAD shim before production use, and avoid running it against untrusted documents on shared machines. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/binbin/docx-cn-1-0-1) <br>
- [Publisher profile](https://clawhub.ai/user/binbin) <br>
- [OpenClaw fork metadata](https://github.com/anthropics/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and XML/JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify DOCX-related files through companion scripts when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
