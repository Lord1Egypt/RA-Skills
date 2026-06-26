## Description: <br>
基于六维人生模型的通用电脑文件自动整理技能，支持语义分类、集合格文件夹、按需创建目录等规则。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keson1521](https://clawhub.ai/user/keson1521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal productivity agents use this skill to organize a chosen local folder by semantic file-name classification into the Six Dimensions of Life folder system, creating folders and moving or renaming files without deleting them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bulk move and rename local files, and incorrect semantic classification could displace files. <br>
Mitigation: Run it only on a specific folder, keep backups of important files, and request a move log so changes can be reviewed or reversed. <br>
Risk: The skill does not require a preview before moves or renames. <br>
Mitigation: Ask the agent to show a preview plan before execution and approve the plan before any filesystem changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keson1521/file-steward) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown report with file organization guidance, move or rename actions, and created-directory details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May move, rename, and create local filesystem entries; the skill states that file deletion is not permitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
