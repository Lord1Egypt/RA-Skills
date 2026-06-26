## Description: <br>
Text-to-speech conversion using uvx edge-tts for generating audio from text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[al-one](https://clawhub.ai/user/al-one) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to convert requested text into spoken audio, including voice, speed, pitch, volume, and subtitle options. It is useful when audio output is preferred for accessibility, multitasking, or hands-free consumption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation may be processed by Microsoft's online TTS service. <br>
Mitigation: Avoid converting secrets, credentials, confidential documents, regulated data, or private messages unless that external processing is acceptable. <br>
Risk: The skill depends on running uvx edge-tts in the agent environment. <br>
Mitigation: Confirm uvx is available and review the generated shell command before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/al-one/edge-tts-uvx) <br>
- [Publisher profile](https://clawhub.ai/user/al-one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of uvx edge-tts to produce audio media files and optional subtitles.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
