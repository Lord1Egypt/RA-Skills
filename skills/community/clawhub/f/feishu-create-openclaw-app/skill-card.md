## Description: <br>
Automates creating and configuring a Feishu or Lark enterprise self-built application for OpenClaw integration via browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diluke1600](https://clawhub.ai/user/diluke1600) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators authorized to manage Feishu or Lark enterprise applications use this skill to create an OpenClaw integration app, import required permissions, and collect the App ID and App Secret for configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow applies broad Feishu or Lark enterprise permissions. <br>
Mitigation: Review and reduce the permission list before granting access, and require explicit administrator approval before applying permissions. <br>
Risk: The workflow can reveal a full App Secret in chat. <br>
Mitigation: Avoid printing the App Secret into chat; copy it directly into secure configuration storage and rotate it if it has already been exposed. <br>
Risk: The skill is intended for enterprise app administration. <br>
Mitigation: Install and run it only when the operator is authorized to administer Feishu or Lark enterprise apps. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/diluke1600/feishu-create-openclaw-app) <br>
- [Feishu Developer Console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with browser actions, JSON permissions, and credential output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive Feishu App ID and App Secret values after successful setup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
