## Description: <br>
Organize the Downloads folder into a clean, searchable command center by file type, project, date, and action state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users use this skill to plan and preview organization of a local Downloads folder by file type, project, date, and action state before applying file moves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Explicit apply mode can move local files into new category folders. <br>
Mitigation: Start in preview mode, verify the target folder and generated move list, and use --apply only after user confirmation. <br>
Risk: A broad or incorrect target folder could produce an unwanted organization plan. <br>
Mitigation: Ask for the exact folder path when missing and keep the file scope explicit before proposing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/downloads-command-center) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON preview output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview-first workflow; explicit user confirmation is expected before applying file moves.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG; artifact frontmatter declares 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
