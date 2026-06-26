## Description: <br>
feishu-im helps agents use Feishu/Lark IM APIs for message sending, chat creation, pinning, urgent notifications, recalls, group menus, tabs, announcements, and related group-management tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyyao2222-eng](https://clawhub.ai/user/sunnyyao2222-eng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide Feishu/Lark bot integrations that send messages, manage group chats, update announcements, configure chat UI surfaces, and handle common IM API errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers powerful Feishu/Lark messaging and group-management actions that can affect users and chat spaces. <br>
Mitigation: Install only for agents that should operate a Feishu/Lark bot with messaging and group-management authority. <br>
Risk: Overbroad app permissions could allow message recall, group creation, member changes, announcements, urgent/system messages, or chat UI changes outside the intended workflow. <br>
Mitigation: Configure the Feishu app with the narrowest permissions needed and require explicit user approval for high-impact chat actions. <br>
Risk: Misuse or exposure of a tenant access token could enable unauthorized Feishu API calls. <br>
Mitigation: Store tenant access tokens in the agent runtime's secret manager and avoid placing tokens in prompts, logs, or generated artifacts. <br>


## Reference(s): <br>
- [Feishu IM Open API](https://open.feishu.cn/open-apis/im/v1) <br>
- [ClawHub skill page](https://clawhub.ai/sunnyyao2222-eng/feishu-im) <br>
- [Publisher profile](https://clawhub.ai/user/sunnyyao2222-eng) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, JSON] <br>
**Output Format:** [Markdown reference with HTTP endpoints, permission notes, and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers Feishu/Lark messaging, group-management, chat UI configuration, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
