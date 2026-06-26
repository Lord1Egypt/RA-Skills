## Description: <br>
Converts text to speech with MOSS-TTS and sends the resulting voice message to a Feishu chat or user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloeveryworlds](https://clawhub.ai/user/helloeveryworlds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate spoken audio from text and send it through Feishu as a bot voice message. It can also retrieve recent Feishu chat history when the corresponding permissions are granted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Feishu credentials that can send messages and may read chat history if history lookup is used. <br>
Mitigation: Limit Feishu app scopes to the sending workflow unless history lookup is needed, and grant chat-history permissions only to approved workspaces and chats. <br>
Risk: Text submitted for speech generation is sent to the external MOSS-TTS provider. <br>
Mitigation: Avoid sending sensitive or regulated text through the TTS workflow unless the provider and data handling terms are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/helloeveryworlds/feishu-voice-tts) <br>
- [Feishu tenant token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu messages API endpoint](https://open.feishu.cn/open-apis/im/v1/messages) <br>
- [MOSS-TTS API endpoint](https://studio.mosi.cn/v1/audio/tts) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu voice-message workflow guidance and script invocations; runtime scripts can create WAV and OPUS audio files before sending them through Feishu.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
