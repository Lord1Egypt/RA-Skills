## Description: <br>
Feishu (Lark) Bot integration for messaging, group management, and approval workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation teams use this skill to let an agent send Feishu/Lark messages, manage chats, and create or query approval workflows through a configured Feishu app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real Feishu/Lark messages, manage chats, and trigger approval workflows with the configured app permissions. <br>
Mitigation: Use a dedicated low-privilege Feishu/Lark app, grant only required scopes, and require review of recipients, chat membership changes, and approval actions before execution. <br>
Risk: Webhook sending accepts caller-provided webhook URLs. <br>
Mitigation: Restrict webhook URLs operationally to trusted Feishu/Lark endpoints. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Feishu API Documentation](https://open.feishu.cn/document) <br>
- [Bot Development Guide](https://open.feishu.cn/document/home/introduction-to-feishu-platform/bot-development-odyssey) <br>
- [ClawHub Skill Page](https://clawhub.ai/jason-aka-chen/feishu-bot-chen) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python examples, shell commands, and JSON-like API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Feishu app ID and app secret configured through environment variables or agent settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
