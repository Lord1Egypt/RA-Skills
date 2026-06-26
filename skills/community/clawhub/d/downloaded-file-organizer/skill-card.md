## Description: <br>
Organize files from the Downloads folder into appropriate local directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XuXinyuan2019](https://clawhub.ai/user/XuXinyuan2019) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to review a dry-run plan for sorting Downloads files, confirm or adjust destinations, and then execute the move with logs and an index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move local files from the Downloads folder, including through optional watch mode. <br>
Mitigation: Review the dry-run plan before execution and avoid watch mode for sensitive or actively changing Downloads folders. <br>
Risk: The skill keeps persistent logs and updates a filename index beyond the immediate move operation. <br>
Mitigation: Use it only where filename retention is acceptable, and consider disabling broad indexing if logs or indexes would expose sensitive filenames. <br>
Risk: Broad source and destination configuration can affect unintended local paths. <br>
Mitigation: Review configuration before use and add source and destination path validation if deploying in a shared or sensitive environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/XuXinyuan2019/downloaded-file-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON execution plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce file move plans, execution summaries, persistent logs, and a local filename index.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
