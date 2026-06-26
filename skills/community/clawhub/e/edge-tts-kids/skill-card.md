## Description: <br>
Edge TTS 中文定制版，提供成人和儿童中文配音预设，并生成 MP3 音频发送到对话。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn Chinese text into voiceover audio with preset adult and child-style voices for stories, narration, education, and similar content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation may be processed by Microsoft Edge TTS. <br>
Mitigation: Avoid sensitive or confidential text unless external TTS processing is acceptable for the user's environment. <br>
Risk: Generated MP3 files are posted into the current conversation. <br>
Mitigation: Use explicit prompts for TTS requests and review the destination before sharing generated audio. <br>
Risk: The skill depends on referenced Edge TTS tooling and the node-edge-tts package. <br>
Mitigation: Review or pin the dependency before deployment in stricter environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/systiger/edge-tts-kids) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with JavaScript and bash snippets; generated audio is MP3.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated MP3 files are sent back into the current conversation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill-info.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
