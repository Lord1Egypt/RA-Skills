## Description: <br>
Split large files into smaller chunks with semantic boundary detection for JSON, Markdown, and TXT files while preserving natural boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[expeditionhub](https://clawhub.ai/user/expeditionhub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data practitioners, and agent users use this skill to split large local JSON, Markdown, or text files into smaller chunks for downstream processing, analysis, or corpus preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes split output files to a local directory, so vague or mistaken folder selections can create unexpected files. <br>
Mitigation: Use explicit input and output folders, prefer an empty output directory, and run with --dry-run before writing chunks. <br>


## Reference(s): <br>
- [File Splitter on ClawHub](https://clawhub.ai/expeditionhub/file-splitter) <br>
- [Publisher profile: expeditionhub](https://clawhub.ai/user/expeditionhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated output files are JSON, Markdown, or TXT chunks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The tool writes chunk files to the selected output directory and can preview planned writes with --dry-run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
