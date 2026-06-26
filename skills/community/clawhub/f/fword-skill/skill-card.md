## Description: <br>
AI-powered bidirectional Word-to-LaTeX converter that supports multiple AI providers and can convert LaTeX back to Word while preserving original styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinzhengxu](https://clawhub.ai/user/jinzhengxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and document authors use this skill to convert Word documents to LaTeX for editing or publication workflows, then convert LaTeX back to Word when a styled .docx output is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document content may be sent to the selected AI provider during refinement. <br>
Mitigation: Use trusted AI endpoints and scoped API keys, or run with --raw for documents that should remain local. <br>
Risk: The setup script may install dependencies through system package managers or sudo. <br>
Mitigation: Review setup.sh before running it and install dependencies manually if the environment requires tighter control. <br>
Risk: The .fword workspace stores a copy of the original Word document for style-preserving back-conversion. <br>
Mitigation: Delete the .fword workspace when style recovery is no longer needed. <br>


## Reference(s): <br>
- [Fword Usage Reference](references/usage.md) <br>
- [Pandoc installation documentation](https://pandoc.org/installing.html) <br>
- [Fword Skill on ClawHub](https://clawhub.ai/jinzhengxu/fword-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated .tex or .docx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a .fword workspace, extracted media, LaTeX files, Word documents, and optional raw intermediate LaTeX.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
