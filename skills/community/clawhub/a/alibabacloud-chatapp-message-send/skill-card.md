## Description: <br>
Send WhatsApp messages via Alibaba Cloud Chat App Message Service (CAMS), including template messages, custom messages, template listing, and template detail lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send Alibaba Cloud CAMS WhatsApp messages, list approved templates, inspect template variables, and prepare valid CLI invocations with confirmation before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud credentials or OAuth tokens could be exposed or misused during setup. <br>
Mitigation: Use a least-privilege RAM user, avoid root or long-lived credentials where possible, and never paste real secrets into the agent conversation or command history. <br>
Risk: The skill can send WhatsApp messages from the user's Alibaba Cloud account, including automated or mass-message workflows. <br>
Mitigation: Confirm sender, recipient, template, language, parameters, and content before sending; use dry-run previews and avoid --yes unless intentionally automating. <br>
Risk: Overbroad CAMS permissions can expand impact if credentials are compromised. <br>
Mitigation: Review the referenced RAM policy and grant only the CAMS permissions needed for sending messages and reading template details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-chatapp-message-send) <br>
- [Aliyun CLI installation guide](references/cli-installation-guide.md) <br>
- [RAM permission policies](references/ram-policies.md) <br>
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/) <br>
- [Chat App Message Service console](https://cams.console.aliyun.com/) <br>
- [SendChatappMessage API documentation](https://www.alibabacloud.com/help/zh/chatapp/developer-reference/api-cams-2020-06-06-sendchatappmessage) <br>
- [ListChatappTemplate API documentation](https://www.alibabacloud.com/help/zh/chatapp/developer-reference/api-cams-2020-06-06-listchatapptemplate) <br>
- [GetChatappTemplateDetail API documentation](https://www.alibabacloud.com/help/zh/chatapp/developer-reference/api-cams-2020-06-06-getchatapptemplatedetail) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Aliyun CLI wrapper scripts and return text or JSON command results.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
