## Description: <br>
Clawatar gives an AI agent a local 3D VRM avatar viewer with animations, expressions, voice chat, TTS lip sync, and WebSocket control. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[Dongping-Chen](https://clawhub.ai/user/Dongping-Chen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Clawatar to install and control a local visual avatar companion for VRM display, avatar actions, expressions, voice chat, and TTS lip sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requires review because it runs unpinned remote npm code and dependencies from the referenced project. <br>
Mitigation: Review the referenced project and npm dependency tree before installation, and prefer a pinned, audited revision for deployment. <br>
Risk: Voice chat and TTS can send audio or text to external services and may expose sensitive conversations. <br>
Mitigation: Use a dedicated ElevenLabs API key, avoid using voice or TTS for secrets, and confirm where audio and text are sent before enabling these features. <br>
Risk: The local WebSocket control surface can trigger avatar actions and speech. <br>
Mitigation: Keep the WebSocket bound to localhost and avoid exposing the control port to untrusted networks. <br>
Risk: The artifact notes Mixamo animations require credit and are non-commercial. <br>
Mitigation: Confirm animation licensing and attribution requirements, or replace the animations, before any commercial use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dongping-Chen/clawatar) <br>
- [Clawatar GitHub project referenced by install instructions](https://github.com/Dongping-Chen/Clawatar.git) <br>
- [Mixamo animation reference](https://www.mixamo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes WebSocket JSON payloads for avatar actions, expressions, reset, and TTS.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
