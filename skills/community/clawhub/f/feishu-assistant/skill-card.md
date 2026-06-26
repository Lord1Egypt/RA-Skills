## Description: <br>
Feishu Assistant sends selected local images to Feishu chats, users, or message threads through a configured Feishu bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gushenjie](https://clawhub.ai/user/gushenjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to send generated or selected local images to Feishu chats, individual users, or message replies through a Feishu bot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images may be sent to the wrong Feishu recipient if chat, user, open, or message IDs are incorrect. <br>
Mitigation: Verify the local image path and intended Feishu recipient identifier before execution, especially for group chats or sensitive images. <br>
Risk: The skill uses Feishu bot credentials to upload and send local images. <br>
Mitigation: Configure credentials only in trusted environments and limit the bot to the intended Feishu application permissions and conversations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gushenjie/feishu-assistant) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local image path and one Feishu recipient identifier such as chat_id, user_id, open_id, or message_id.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
