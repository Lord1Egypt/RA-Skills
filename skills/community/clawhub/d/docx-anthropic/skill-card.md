## Description: <br>
Creates, reads, edits, validates, converts, and manipulates Microsoft Word .docx files, including formatting, comments, images, and tracked changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and document-producing agents use this skill to create polished Word documents, inspect or modify existing DOCX packages, convert documents, and manage tracked changes and comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local document tooling may run LibreOffice operations and use a temporary macro profile plus an LD_PRELOAD native shim for compatibility. <br>
Mitigation: Install and run in a single-user or sandboxed environment, review helper scripts before deployment, and avoid shared systems for untrusted Office files. <br>
Risk: Tracked changes, comments, and Office metadata may preserve sensitive information in generated or edited documents. <br>
Mitigation: Review tracked changes, comments, and document metadata before sharing outputs, and validate generated DOCX files before distribution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, and generated or modified DOCX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local Office tooling such as LibreOffice, pandoc, docx-js, and helper scripts for unpacking, validation, comments, conversion, and tracked changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
