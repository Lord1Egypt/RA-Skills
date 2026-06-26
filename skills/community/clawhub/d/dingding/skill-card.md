## Description: <br>
Dingding helps developers integrate DingTalk Open Platform APIs for bots, approvals, schedules, directory, attendance, OAuth2, and event callbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and enterprise automation teams use this skill for guidance, request examples, and implementation patterns when connecting agents or applications to DingTalk Open Platform workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DingTalk credentials, webhook tokens, and app secrets could be exposed or used with broader permissions than needed. <br>
Mitigation: Use environment variables or a secret manager, avoid hardcoding credentials, and grant only the DingTalk app scopes required for the task. <br>
Risk: The skill can guide sensitive enterprise actions, including sending messages, starting approvals, creating calendar events, or reading directory and attendance records. <br>
Mitigation: Require authorization for the tenant and target users, and ask for explicit confirmation before performing actions that affect users or expose records. <br>
Risk: DingTalk integrations may fail or behave unexpectedly when mixing newer api.dingtalk.com endpoints with legacy oapi.dingtalk.com endpoints. <br>
Mitigation: Confirm endpoint choice against current DingTalk documentation and test flows with non-production data before using real enterprise workflows. <br>


## Reference(s): <br>
- [Dingding ClawHub release](https://clawhub.ai/zhangifonly/dingding) <br>
- [DingTalk Open Platform API base](https://api.dingtalk.com) <br>
- [DingTalk legacy OAPI base](https://oapi.dingtalk.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API endpoints, JSON examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DingTalk request bodies, authentication guidance, event callback notes, and troubleshooting tips.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
