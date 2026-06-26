## Description: <br>
飞书日历管理（中文版）用于查询飞书日程、创建日历事件和查询忙闲状态。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkingmanyangyang](https://clawhub.ai/user/thinkingmanyangyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users with Feishu calendar access use this skill to review schedules, create meetings, and check availability from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth credentials may be handled unsafely, including use of an embedded app secret or saved token file. <br>
Mitigation: Use your own Feishu app credentials, rotate or remove embedded secrets, and protect or delete saved token files after use. <br>
Risk: The skill under-discloses write access while supporting calendar event creation. <br>
Mitigation: Grant only intended Feishu calendar scopes and require explicit user confirmation before creating calendar events. <br>
Risk: Refreshing stored credentials can extend access beyond the immediate task. <br>
Mitigation: Refresh credentials only with user approval and periodically revoke or rotate tokens that are no longer needed. <br>


## Reference(s): <br>
- [飞书日历 OAuth 配置指南](references/oauth-setup.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [ClawHub skill page](https://clawhub.ai/thinkingmanyangyang/feishu-calendar-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu OAuth credentials and can read, create, or refresh calendar-related data depending on the invoked workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
