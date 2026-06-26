## Description: <br>
Converts Word (.docx) documents to Markdown and extracts embedded images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ooliuhao](https://clawhub.ai/user/ooliuhao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, technical writers, and content maintainers use this skill to convert .docx files into Markdown while saving embedded images for reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A specially crafted DOCX file could cause local files to be moved outside the intended output area. <br>
Mitigation: Review or patch the script before using it on untrusted DOCX files; normalize and validate archive member paths and keep writes inside the chosen output directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ooliuhao/docx-to-md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands] <br>
**Output Format:** [Markdown files, extracted image files, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.7+ and python-docx; accepts an input .docx path and optional output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
