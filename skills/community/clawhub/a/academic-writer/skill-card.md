## Description: <br>
Professional LaTeX writing assistant. Capabilities include: scanning existing LaTeX templates, reading reference materials (Word/Text), drafting content strictly following templates, and compiling PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dayunyan](https://clawhub.ai/user/dayunyan) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Students, researchers, and technical authors use this skill to analyze LaTeX templates, load reference materials, draft LaTeX content, maintain citation handoffs, and compile academic PDFs in a Linux or WSL2 project workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local reference files, modify LaTeX project files, and run local LaTeX compilation. <br>
Mitigation: Use it in a dedicated trusted project folder, avoid absolute or parent-directory paths unless intentional, and review diffs or backups before accepting overwrites. <br>
Risk: Compiling untrusted TeX templates or project files can expose the user to unsafe local behavior. <br>
Mitigation: Compile only trusted templates and TeX files, and inspect unfamiliar inputs before running the compilation workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dayunyan/academic-writer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with LaTeX code, shell commands, and file-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read reference files, write LaTeX project files, and report PDF compilation results when its local helper script is executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
