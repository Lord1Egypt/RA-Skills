## Description: <br>
每日学习卡片 turns OpenClaw conversation history into daily learning cards, weekly summaries, and weekly quiz questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlarkspur](https://clawhub.ai/user/vlarkspur) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to convert recurring chat history from Feishu, WebUI, DingTalk, WeCom, and QQBot into structured learning notes, daily Markdown cards, Feishu notifications, weekly summaries, and weekly quizzes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes OpenClaw chat history and learning notes through recurring automation. <br>
Mitigation: Use it only with conversations approved for local storage and automated summarization, and define retention and redaction rules before enabling schedules. <br>
Risk: Generated summaries and quiz content can be sent to Feishu targets. <br>
Mitigation: Replace hard-coded delivery targets with explicit approved recipients and review channel configuration before installation. <br>
Risk: Weekly summary and quiz generation can send learning data to third-party AI endpoints. <br>
Mitigation: Replace hard-coded API credentials, require HTTPS endpoints, and confirm the endpoint is approved for the data being processed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlarkspur/daily-learning-cards) <br>
- [Publisher profile](https://clawhub.ai/user/vlarkspur) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown learning cards and summaries, Feishu-ready message text, quiz Markdown, shell commands, and JSON configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes learning cards, weekly summaries, and quiz files under the OpenClaw workspace memory directories and can schedule recurring delivery jobs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
