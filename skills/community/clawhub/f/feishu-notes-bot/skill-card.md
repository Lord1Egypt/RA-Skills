## Description: <br>
通过飞书机器人创建、查询和管理笔记，支持飞书消息交互和云文档同步。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilinkzwq](https://clawhub.ai/user/ilinkzwq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams use this skill to configure a Feishu bot that creates, searches, and manages meeting notes, quick notes, project notes, and action items from Feishu chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected notes, meeting records, and project content may be sent to Feishu or stored locally. <br>
Mitigation: Use a dedicated Feishu app, grant only required permissions, review document sharing settings, and avoid sending sensitive content unless the workspace is approved for it. <br>
Risk: Feishu App Secret exposure could allow unauthorized API use. <br>
Mitigation: Keep FEISHU_APP_SECRET private, use environment variables or protected configuration, and rotate credentials if exposure is suspected. <br>
Risk: Separate helper scripts or gateway services may run with real Feishu credentials. <br>
Mitigation: Inspect helper scripts and gateway services before running them with production credentials. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Feishu API Documentation](https://open.feishu.cn/document/) <br>
- [ClawHub Skill Page](https://clawhub.ai/ilinkzwq/feishu-notes-bot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and note templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus FEISHU_APP_ID and FEISHU_APP_SECRET for Feishu API setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
