## Description: <br>
Converts selected text into Chinese speech with Edge TTS and sends it as a native Feishu voice message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmx0632](https://clawhub.ai/user/xmx0632) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and Feishu bot operators use this skill to generate short voice replies or notifications from text and deliver them through Feishu chats. It is intended for conversational voice responses, voice notifications, and situations where spoken output is preferred over text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected chat text may be sent to Microsoft TTS for speech generation. <br>
Mitigation: Avoid sensitive or regulated text and require explicit user confirmation or a dedicated command prefix before generating voice output. <br>
Risk: Generated audio can be sent automatically through a configured Feishu bot. <br>
Mitigation: Use limited Feishu bot permissions and review the target chat or recipient before enabling automated voice replies. <br>
Risk: The installation flow uses an unpinned edge-tts dependency. <br>
Mitigation: Review and pin an approved edge-tts version before deployment in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xmx0632/feishu-voice-reply) <br>
- [edge-tts on PyPI](https://pypi.org/project/edge-tts/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates MP3 audio files through edge-tts and can send them through the OpenClaw Feishu message tool.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
