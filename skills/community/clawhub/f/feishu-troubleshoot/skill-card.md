## Description: <br>
Helps agents guide users through OpenClaw and Feishu connection troubleshooting, including bot setup, event subscription, application publishing, and required permission scopes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TinaDu-AI](https://clawhub.ai/user/TinaDu-AI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace administrators use this skill when configuring or troubleshooting an OpenClaw bot integration with Feishu. It provides concise setup guidance and permission JSON for bot messaging, long-connection event handling, calendar access, and task access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to grant broad Feishu workspace permissions for messaging, calendar, task, and contact access. <br>
Mitigation: Have a Feishu administrator review each scope, import only the permissions needed for the deployment, and test first in a limited app or workspace. <br>
Risk: Message-event and long-connection setup may expose operational messages or logs through the OpenClaw gateway. <br>
Mitigation: Confirm how the gateway handles message events and logs before enabling event subscriptions in a production workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TinaDu-AI/feishu-troubleshoot) <br>
- [飞书开放平台](https://open.feishu.cn/app) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, JSON] <br>
**Output Format:** [Markdown with JSON permission examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only troubleshooting guidance; users should review permission scopes before applying them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
