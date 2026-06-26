## Description: <br>
Feishu Notify sends text, rich text, interactive card, and image notifications to Feishu (Lark) chats through configured webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex098929](https://clawhub.ai/user/alex098929) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send operational alerts, status updates, task notifications, and other messages from an agent workflow to configured Feishu chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured Feishu webhook URLs can post to chats and should be treated as secrets. <br>
Mitigation: Store webhook URLs only in the user configuration file with restricted permissions, do not commit them, and rotate any exposed URLs. <br>
Risk: An agent using this skill may send messages to sensitive channels or include sensitive content. <br>
Mitigation: Ask the agent to preview the destination and message content, and require confirmation for sensitive or important notifications. <br>
Risk: Message templates influence the JSON payload sent to Feishu. <br>
Mitigation: Use templates from the bundled templates directory and avoid arbitrary external JSON templates. <br>


## Reference(s): <br>
- [Feishu Webhook API Documentation](references/api_documentation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON message payloads and command-line script invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send webhook POST requests to configured Feishu chats and returns delivery status or error details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
