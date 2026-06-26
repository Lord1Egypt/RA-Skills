## Description: <br>
Manages Feishu calendars and events, including listing calendars and querying, creating, updating, deleting, recurring, reminder, timezone, and all-day event workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TEweitao](https://clawhub.ai/user/TEweitao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to Feishu Calendar through their own Feishu app credentials, then read calendars and manage event records. It is suited for productivity workflows that need calendar lookup, scheduling, updates, deletion, recurrence, reminders, timezone handling, and all-day events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive calendar content such as event titles, descriptions, locations, attendees, and timing. <br>
Mitigation: Treat calendar data as sensitive and limit agent access, logs, prompts, and downstream sharing to the minimum needed for the workflow. <br>
Risk: Feishu App Secret or tenant access tokens could be leaked if committed, pasted into prompts, or logged. <br>
Mitigation: Store credentials in environment variables or a secrets manager, never commit secrets, and rotate credentials if exposure is suspected. <br>
Risk: Calendar create, update, and delete operations can alter real user or company schedules. <br>
Mitigation: Grant only required Feishu calendar scopes and require explicit user confirmation before mutating or deleting events. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TEweitao/feishu-calendar-event) <br>
- [Feishu Calendar API documentation](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/calendar-v4/calendar/list) <br>
- [Feishu tenant access token documentation](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/authentication-management/auth-v3/auth-v3-tenant_access_token) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JavaScript, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Feishu calendar identifiers, event titles, descriptions, locations, timestamps, recurrence rules, reminders, and API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
