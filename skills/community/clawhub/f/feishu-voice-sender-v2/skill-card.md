## Description: <br>
Sends Feishu voice-message responses by selecting a channel-specific path and using Xiaomi MiMo TTS for Feishu audio generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EnderXiao](https://clawhub.ai/user/EnderXiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to generate voice responses for Feishu channels and fall back to channel-appropriate behavior for other messaging platforms. It is intended for workflows where an agent needs to turn user-provided text into a voice notification or reply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text may be sent to an external Xiaomi MiMo TTS path. <br>
Mitigation: Use the skill only with approved text data, disclose the external TTS dependency, and configure a dedicated MiMo API key. <br>
Risk: The Feishu send path can report delivery success even though the send implementation is not complete. <br>
Mitigation: Review or fix the send implementation before deployment and verify actual Feishu delivery before reporting success to users. <br>
Risk: Automatic channel detection can generate or attempt to send voice messages unexpectedly. <br>
Mitigation: Require explicit confirmation before generating or sending voice messages and use least-privilege Feishu bot credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EnderXiao/feishu-voice-sender-v2) <br>
- [Xiaomi MiMo API Platform](https://platform.xiaomimimo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance, command-line status text, and generated voice audio files when the helper succeeds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MIMO_API_KEY, ffmpeg, the Xiaomi MiMo TTS skill, and approved Feishu bot credentials for deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
