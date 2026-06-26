## Description: <br>
文档格式刷 helps an agent extract or apply document formatting across Word, Markdown, and plain text files, including template-based formatting, heading-level recognition, and the built-in GB/T 9704-2012 official document style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yechao1995](https://clawhub.ai/user/yechao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to reformat a document to match a Word template, apply official Chinese document formatting, or convert formatted content among .docx, .md, and .txt outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite or create local document outputs at user-provided paths. <br>
Mitigation: Use clear input and output paths, keep backups before writing over important documents, and avoid targeting files that are open in Word. <br>
Risk: Extracted format JSON from confidential templates can include local paths and short text snippets. <br>
Mitigation: Treat generated format profiles as sensitive when templates are confidential and avoid sharing them outside the intended workspace. <br>
Risk: Runtime use may require python-docx. <br>
Mitigation: Install python-docx only from a trusted package source when the runtime requires it. <br>


## Reference(s): <br>
- [文档格式刷 reference manual](references/format_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/yechao1995/doc-format-brush) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown guidance with bash commands and generated document or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local .docx, .md, .txt, or format-profile JSON files based on user-selected input and output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
