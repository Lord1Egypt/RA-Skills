## Description: <br>
英语口语练习助手，包含对话训练和任务推送两大功能。需要用户发送语音或文字消息且内容与英语练习相关时触发对话训练；定时触发任务推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsy000](https://clawhub.ai/user/zsy000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to practice everyday English speaking through voice or text conversations, with translation, speaking feedback, vocabulary support, and optional daily phrase pushes. Operators can configure local practice records and scheduled outbound messages for a selected user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration can contain an API key and a custom API endpoint. <br>
Mitigation: Keep config.json private, use a limited API key, and verify the endpoint before enabling API-backed push or summary generation. <br>
Risk: Optional cron jobs can send automated outbound English-learning messages. <br>
Mitigation: Enable scheduled pushes or monthly summaries only when automated messages are desired, and verify the target user ID and channel first. <br>
Risk: The skill writes local practice history and push records. <br>
Mitigation: Choose an appropriate data directory and review stored practice data according to the user's privacy expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zsy000/english-speaking-practice) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text and Markdown, with optional shell commands and JSON-backed local practice records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured speech, message, and model services; optional scheduled pushes can send outbound messages and write local monthly practice data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
