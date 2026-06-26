## Description: <br>
This skill helps agents send Feishu messages, look up chat and member identifiers, retrieve chat lists and group members, and use Feishu messaging API examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[make453](https://clawhub.ai/user/make453) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workplace automation users use this skill to automate Feishu messaging workflows, including finding recipients or chats and preparing API calls for text, image, and file messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled scripts include hardcoded Feishu credentials. <br>
Mitigation: Remove embedded credentials, rotate any exposed secrets, and provide least-privilege Feishu app credentials through environment variables or another secret manager. <br>
Risk: Directory lookups can expose employee data such as phone, email, employee number, or department. <br>
Mitigation: Use directory lookup only with explicit authorization and avoid printing or sharing personal data unless required for the approved workflow. <br>
Risk: Messaging and upload actions can send content to the wrong recipient or channel. <br>
Mitigation: Confirm every recipient, message body, and upload manually before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/make453/feishu-messaging-bak) <br>
- [Feishu Open Platform API documentation](https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list) <br>
- [Feishu web app](https://www.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu API request examples and command-line script usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
