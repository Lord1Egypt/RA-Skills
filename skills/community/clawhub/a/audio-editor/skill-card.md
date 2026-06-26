## Description: <br>
Perform audio editing tasks including trimming, volume adjustment, format conversion, and extracting audio from video files using natural language commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwl1992](https://clawhub.ai/user/jwl1992) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and audio workflow users can use this skill to request common audio edits, such as extracting audio from video, adjusting volume, converting formats, and producing an edited audio file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the shell helper can execute arbitrary commands instead of staying limited to audio processing. <br>
Mitigation: Remove eval, reject unsupported natural-language requests, validate file paths and numeric values, and invoke ffmpeg through safely quoted arguments before running this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jwl1992/audio-editor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text command output and resulting audio file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg >= 5.0; default output path is ~/openclaw_audio.mp3 when no output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
