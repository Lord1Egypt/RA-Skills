## Description:

自动化完成飞书开放平台企业自建应用的创建、权限配置、事件订阅、改名和版本发布，简化繁琐操作流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[evan966890](https://clawhub.ai/user/evan966890)

### License/Terms of Use:


## Use Case:

Developers and Feishu enterprise administrators use this skill to automate setup of a Feishu/OpenClaw bot application, including app creation, permission import, event subscription, naming, release publication, and local OpenClaw configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks administrators to grant broad Feishu production permissions for messaging, contacts, application management, events, and file access.

Mitigation: Review and minimize every requested permission, confirm the data range and business need with a Feishu administrator, and publish only the scopes that are required.

Risk: The workflow requires handling the Feishu App Secret, which is a credential.

Mitigation: Do not paste the App Secret into chat or logs; store it only in a protected secret store or secured configuration and rotate it if exposed.

Risk: Browser automation can publish application changes or select the wrong control if page state, element references, or permissions differ from the documented flow.

Mitigation: Run the automation in an authenticated administrator session with human review at permission import, data-range confirmation, secret display, and final publish steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evan966890/skills/feishu-app-setup)
- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, JavaScript, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes procedural browser-automation steps and operational cautions for Feishu app setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
