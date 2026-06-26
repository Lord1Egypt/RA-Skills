## Description: <br>
Extracts archive files and sorts their contents into user-selected directories based on filename keyword rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zj-zc](https://clawhub.ai/user/zj-zc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to preview and execute archive extraction and file classification workflows. It helps organize files from zip, tar, 7z, and rar archives into configured destination folders using reusable keyword rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rule-controlled target paths may move files outside the intended organization pattern or destination structure. <br>
Mitigation: Review data/rules.json before execution and keep target directories to simple relative names under the chosen output folder. <br>
Risk: Executing classification can move or overwrite files. <br>
Mitigation: Run preview mode first, confirm the generated classification report, and avoid overwrite mode unless the destination has been reviewed. <br>
Risk: Password-protected 7z/rar archives or optional archive-tool installs can add handling uncertainty. <br>
Mitigation: Use caution with protected archives and only install or invoke optional archive tools when the source and archive contents are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zj-zc/compress-file-sorter) <br>
- [Publisher profile](https://clawhub.ai/user/zj-zc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with shell commands and JSON rule configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May move or copy files after user confirmation; preview mode reports planned classifications without moving files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
