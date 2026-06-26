## Description: <br>
Generates speech with Microsoft Edge TTS and sends it as a Feishu audio message when a user asks for voice replies, voice messages, or TTS reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and operators use this skill to convert user-provided text into Chinese speech and send it to a Feishu recipient as a voice message. It is useful when a conversation should continue through Feishu audio instead of plain text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text sent through this skill is processed by Edge TTS and Feishu before delivery. <br>
Mitigation: Use it only when those services are acceptable for the message content, and avoid sending secrets or sensitive internal text. <br>
Risk: The skill uses Feishu app credentials and sends messages to a supplied recipient. <br>
Mitigation: Use least-privilege Feishu app credentials and verify the recipient open_id and message content before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dadaniya99/feishu-edge-tts-voice) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in an external Feishu audio message when run with valid Feishu app credentials and a recipient open_id.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
