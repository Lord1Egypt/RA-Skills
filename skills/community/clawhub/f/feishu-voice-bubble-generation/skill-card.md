## Description: <br>
Helps a Feishu agent turn text into MP3, convert it to Opus, and send the Opus file as a native Feishu voice bubble. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lens-lzy](https://clawhub.ai/user/lens-lzy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu agent operators use this skill to generate Chinese speech from text, convert audio to the Opus format expected by Feishu voice bubbles, and send the resulting audio after confirming the target chat and message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer adds audio-generation and conversion dependencies using pip and a system package manager. <br>
Mitigation: Review setup.sh before installation and install only in an environment where edge-tts and ffmpeg are expected. <br>
Risk: Generated audio could be sent to an unintended Feishu chat or with unintended content. <br>
Mitigation: Require explicit confirmation of the target chat and message before sending generated audio or onboarding voice samples. <br>
Risk: Feishu voice bubbles require Opus audio; sending the intermediate MP3 changes the user experience by sending an attachment instead. <br>
Mitigation: Use MP3 only as an intermediate file and send the converted Opus file unless the user explicitly asks for the MP3. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lens-lzy/feishu-voice-bubble-generation) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for generating MP3 audio, converting it to Opus, selecting Chinese TTS voices, and sending only the Opus output as a Feishu voice bubble by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
