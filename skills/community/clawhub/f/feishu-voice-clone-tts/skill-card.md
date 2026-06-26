## Description: <br>
Converts text to speech with Volcengine TTS using preset or cloned voices and sends the generated audio to Feishu chats or groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willsonchenservice-eng](https://clawhub.ai/user/willsonchenservice-eng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to generate spoken messages from text and deliver them into Feishu one-on-one chats or groups. It is useful for agent workflows that need voice notifications or voice-message delivery through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text is sent to Volcengine for speech synthesis and generated audio is sent to Feishu. <br>
Mitigation: Use only approved text, accounts, and chat destinations; confirm the target chat before sending. <br>
Risk: Feishu and Volcengine credentials are required for runtime operation. <br>
Mitigation: Use least-privileged Feishu credentials, protect VOLC_API_KEY and any ~/.volcengine_key file, and avoid exposing secrets in logs or shared environments. <br>
Risk: Voice cloning can reproduce a person's voice. <br>
Mitigation: Use cloned voices only with proper authorization and consent. <br>
Risk: A configurable VOLC_TTS_URL could route speech requests to an unintended endpoint. <br>
Mitigation: Keep VOLC_TTS_URL unset or restrict it to a trusted official endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/willsonchenservice-eng/feishu-voice-clone-tts) <br>
- [Volcengine TTS console](https://console.volcengine.com/speech/new/experience/tts?projectName=default) <br>
- [Volcengine voice clone console](https://console.volcengine.com/speech/new/experience/clone?projectName=default) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Audio messages] <br>
**Output Format:** [Markdown guidance with inline shell commands and runtime audio delivery through Feishu] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu credentials, a Volcengine API key, a voice type, and ffmpeg/ffprobe at runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
