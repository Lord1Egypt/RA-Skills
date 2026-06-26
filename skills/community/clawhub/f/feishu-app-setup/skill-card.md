## Description: <br>
自动化完成飞书开放平台企业自建应用的创建、权限配置、事件订阅、改名和版本发布，简化繁琐操作流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evan966890](https://clawhub.ai/user/evan966890) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Feishu workspace administrators use this skill to guide an agent through browser-based setup of an enterprise Feishu app, including bot capability, permissions, event subscriptions, naming, publishing, and OpenClaw Gateway configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an authenticated Feishu administrator session to grant broad application permissions and publish live tenant changes. <br>
Mitigation: Use a test tenant or a dedicated least-privilege admin account, review requested scopes before importing them, and manually confirm permission and publication steps. <br>
Risk: App Secret values may be exposed during browser automation, logs, or chat transcripts. <br>
Mitigation: Avoid displaying or pasting secrets into shared logs or chats, keep credentials out of version control, and rotate credentials if exposure is suspected. <br>
Risk: Event subscription changes depend on an active OpenClaw Gateway WebSocket connection and can fail or leave the app partially configured. <br>
Mitigation: Configure the app credentials, restart the gateway, verify the active connection, and then save the Feishu event subscription. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evan966890/feishu-app-setup) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, JavaScript, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes browser automation steps, permission scope examples, event subscription guidance, and OpenClaw configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
