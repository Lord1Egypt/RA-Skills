## Description: <br>
Generates dictation audio from English word lists, reading each word twice with a one-second pause. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[effeceee](https://clawhub.ai/user/effeceee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners, educators, and developers use this skill to turn English vocabulary lists into repeated MP3 dictation practice audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input words may be processed by the configured text-to-speech provider. <br>
Mitigation: Avoid confidential words or names unless you accept the provider's data handling. <br>
Risk: The skill depends on edge-tts and ffmpeg binaries. <br>
Mitigation: Install dependencies from trusted sources and review generated commands before execution. <br>
Risk: Each run writes to /tmp/dictation.mp3 and may replace an existing file. <br>
Mitigation: Move or rename any existing /tmp/dictation.mp3 file before running if it should be preserved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/effeceee/dictation-audio) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated runtime output is an MP3 file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires edge-tts and ffmpeg; writes the generated audio to /tmp/dictation.mp3.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
