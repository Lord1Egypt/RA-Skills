## Description: <br>
Use when AudioClaw Skills, Feishu, or Lark needs to send AudioClaw voice replies with runtime-switchable voice_id, emotion preset, or speaking style, including per-message speaker overrides, voice-family emotion routing, cache reuse, and safe fallback when a requested voice is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AudioClaw operators use this skill to turn final assistant text into voice replies, choose or remember voice settings, and deliver Feishu or Lark-friendly audio. It is intended for workflows that need dynamic voice selection, fallback handling, caching, and optional direct Feishu audio sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audio can be sent to Feishu using local credentials and an inferred chat destination. <br>
Mitigation: Test with --skip-direct-send first, pass an explicit chat_id for production use, and keep Feishu app permissions narrow. <br>
Risk: Voice generation can send reply text to a cloud TTS provider. <br>
Mitigation: Avoid sending sensitive text unless the deployment has reviewed data handling, consent, and retention requirements. <br>
Risk: Credential and workspace path resolution depends on local helper modules and configuration. <br>
Mitigation: Review the local _shared helper modules and credential files before installation or deployment. <br>
Risk: Requested voices may be unavailable to the current API key and could fall back to another voice. <br>
Mitigation: Use strict_voice or disable fallback when the exact speaker identity is required, and validate voice access at synthesis time. <br>


## Reference(s): <br>
- [OpenClaw Voice Switchboard Reference](references/openclaw_voice_switchboard.md) <br>
- [SenseAudio Text-to-Speech API](https://senseaudio.cn/docs/text_to_speech_api) <br>
- [SenseAudio Voice API](https://senseaudio.cn/docs/voice_api) <br>
- [Feishu Internal Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime scripts can produce a JSON manifest and local audio files for downstream delivery.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
