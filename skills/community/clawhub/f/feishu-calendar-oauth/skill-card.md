## Description: <br>
飞书日历管理技能，支持查询日程、创建、更新、删除事件和设置重复规则。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkingmanyangyang](https://clawhub.ai/user/thinkingmanyangyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to let an agent manage a personal Feishu calendar through OAuth, including schedule lookup, event creation, updates, deletion, recurrence, reminders, and busy/free checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete live Feishu calendar events. <br>
Mitigation: Require confirmation of the event title, time, and event ID before updates or deletions. <br>
Risk: Feishu OAuth credentials are stored in a local plaintext .user_token.json file. <br>
Mitigation: Protect the token file from sharing, backups, logs, and commits. <br>
Risk: Write-level calendar permissions may be broader than needed for lookup-only use. <br>
Mitigation: Prefer read-only calendar permissions when the intended use is only schedule lookup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thinkingmanyangyang/feishu-calendar-oauth) <br>
- [OAuth 配置指南](references/oauth-setup.md) <br>
- [API 使用指南](references/api-guide.md) <br>
- [Feishu Open Platform application console](https://open.feishu.cn/app) <br>
- [Feishu OAuth authorization endpoint](https://accounts.feishu.cn/open-apis/authen/v1/authorize) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with PowerShell command blocks and Feishu API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write Feishu calendar events through OAuth-protected API calls.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
