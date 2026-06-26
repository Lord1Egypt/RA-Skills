## Description: <br>
Send customizable interactive Feishu cards with titles, content, buttons, notes, and color templates to users or group chats via the Feishu Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SeeTheRianBow](https://clawhub.ai/user/SeeTheRianBow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to build or send rich Feishu notifications for tasks, alerts, and group updates from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes built-in Feishu app credentials that may be used if installers do not provide their own. <br>
Mitigation: Set FEISHU_APP_ID and FEISHU_APP_SECRET explicitly and prefer a release that removes embedded credentials before deployment. <br>
Risk: Cards can send content to Feishu users or group chats, so incorrect recipient IDs or sensitive content can expose information. <br>
Mitigation: Confirm recipient IDs carefully and avoid sending secrets, personal data, or regulated business content unless authorized to transmit it to Feishu. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SeeTheRianBow/feishu-cards) <br>
- [Feishu message API endpoint](https://open.feishu.cn/open-apis/im/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline CLI and Python examples plus Feishu card JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send messages through the Feishu Open API when credentials and recipient IDs are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
