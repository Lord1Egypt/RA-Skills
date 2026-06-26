## Description: <br>
Docx Tools helps agents read, write, convert, and merge local DOCX and Markdown documents without network access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to read DOCX content, create or update Word files, convert between DOCX and Markdown, and assemble multi-section documents such as proposals or papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes local DOCX and Markdown files, so incorrect paths could expose or overwrite unintended documents. <br>
Mitigation: Review input and output paths before running conversions or write operations, and avoid sensitive folders unless those documents are intended for processing. <br>
Risk: The skill depends on local Python document-processing packages. <br>
Mitigation: Install dependencies in a virtual environment and review the package set before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jirboy/docx-tools) <br>
- [Publisher profile](https://clawhub.ai/user/jirboy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus generated DOCX or Markdown files when helper scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file reads and writes are expected; output paths should be reviewed before running conversion or write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
