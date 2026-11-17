## Description:

Perform audio editing tasks including trimming, volume adjustment, format conversion, and extracting audio from video files using natural language commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwl1992](https://clawhub.ai/user/jwl1992)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to perform common audio processing tasks, including extracting audio from video, changing volume, converting formats, and producing an output audio path from a natural-language request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an under-disclosed shell execution path that can run arbitrary commands instead of only audio operations.

Mitigation: Review before installing; remove the command execution path, fail closed on unsupported requests, pass ffmpeg arguments safely without eval, and make overwrite behavior explicit and user-controlled.

## Reference(s):

- [Audio Editor ClawHub Skill Page](https://clawhub.ai/jwl1992/skills/audio-editor)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text status messages and an output audio file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg >= 5.0; default output path is ~/openclaw_audio.mp3 unless an output path is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
