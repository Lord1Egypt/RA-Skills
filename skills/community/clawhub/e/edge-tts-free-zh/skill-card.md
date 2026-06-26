## Description: <br>
Configures OpenClaw to use Microsoft Edge text-to-speech for multilingual speech output without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zx0018](https://clawhub.ai/user/zx0018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to enable spoken AI replies through Microsoft Edge TTS, including Chinese and English neural voices. It is most useful for personal assistants, accessibility support, multilingual interactions, and cost-sensitive deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic TTS can send AI reply text to Microsoft's Edge TTS service, which may expose sensitive conversation content. <br>
Mitigation: Use auto=never or auto=mention for sensitive conversations, and enable auto=always only when the user accepts external speech synthesis. <br>
Risk: The install script changes OpenClaw TTS configuration and restarts the gateway. <br>
Mitigation: Review the script before running it, or apply the documented configuration commands manually in controlled environments. <br>
Risk: High-volume use may encounter implicit Microsoft service rate limits. <br>
Mitigation: Avoid bulk synthesis workloads with this skill and monitor TTS failures when usage increases. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zx0018/edge-tts-free-zh) <br>
- [OpenClaw TTS Documentation](https://docs.openclaw.ai/tts) <br>
- [Microsoft Speech Voice Gallery](https://speech.microsoft.com/portal/voicegallery) <br>
- [Edge TTS Python Library](https://github.com/rany2/edge-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configures OpenClaw TTS settings and may restart the OpenClaw gateway when the install script is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
