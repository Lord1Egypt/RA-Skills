## Description: <br>
专为中国CEO打造的AI决策协作体系。主脑+子代理架构，支持飞书通知，定时简报，记忆系统，决策分级管理。5分钟安装，开箱即用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james6548](https://clawhub.ai/user/james6548) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Executives and operators use this skill to coordinate CEO decision support across market monitoring, work tracking, project management, decision archiving, scheduled Feishu briefings, and persistent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses permanent memory for sensitive CEO conversations. <br>
Mitigation: Confirm stored memories can be inspected and deleted, and avoid placing confidential secrets in chat history. <br>
Risk: Scheduled autonomous Feishu reports may send executive or market information to unintended recipients. <br>
Mitigation: Restrict Feishu recipients with allowlists, review scheduled jobs before enabling them, and disable unnecessary reports. <br>
Risk: Feishu document, wiki, drive, and bot access may be broader than required. <br>
Mitigation: Use a least-privilege Feishu app, limit document/wiki/drive scopes, and keep App Secret out of chats and repositories. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/james6548/ceo-ai-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/james6548) <br>
- [ClawHub homepage](https://clawhub.ai) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [README.md](artifact/README.md) <br>
- [CEO决策协作体系v2.8.md](artifact/CEO决策协作体系v2.8.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduled briefing prompts, agent-role guidance, decision-priority guidance, and OpenClaw configuration templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
