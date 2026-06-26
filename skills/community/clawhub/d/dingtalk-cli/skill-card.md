## Description: <br>
当用户提到钉钉知识库、钉钉文档、读取/写入文档、知识库目录、文档成员、`.axls` 表格、workbook、dingtalk doc、wiki workspace 时使用。通过本地 `dingtalk-cli` 命令调用钉钉开放平台 API，适合 agent 直接执行。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianen](https://clawhub.ai/user/ianen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate DingTalk knowledge bases, documents, workbook ranges, and document membership through the local dingtalk-cli command. It is suited to workflows that need authenticated DingTalk reads and deliberate write, delete, or member-management actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables document overwrite, delete, and membership-management actions in DingTalk. <br>
Mitigation: Require the agent to show the exact workspace, node or document key, target user, and planned change before any destructive or access-changing command. <br>
Risk: The skill stores DingTalk app credentials and operator identity in local configuration. <br>
Mitigation: Use least-privilege DingTalk app permissions, protect the saved config file, and prefer environment or filesystem controls that limit credential exposure. <br>
Risk: Using the wrong document mode can lead to failed or repeated operations against .axls workbook nodes. <br>
Mitigation: Use workbook commands for .axls targets and avoid retrying doc read when the CLI reports that the target node is an .axls workbook. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ianen/dingtalk-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to request or use DingTalk credentials and to confirm targets before write, delete, or membership changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
