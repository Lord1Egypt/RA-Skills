## Description: <br>
Feishu Video Editor helps agents run local video-editing workflows for Feishu-shared media, including silence trimming, timestamp cropping, subtitle generation, and audio extraction with FFmpeg and Whisper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to process meeting, lecture, or collaboration videos through an agent interface. It supports common editing tasks such as removing silence, cropping by timestamp, generating SRT subtitles, and extracting audio from local video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-controlled video paths and timestamps can reach shell command execution. <br>
Mitigation: Use only trusted filenames and arguments, and prefer a revised version that replaces shell execution with spawn or execFile argument arrays plus input validation. <br>
Risk: The skill writes local output and temporary processing files during video editing. <br>
Mitigation: Run it in a dedicated workspace or account without sensitive write access, and review configured output paths before use. <br>
Risk: Documentation advertises Feishu upload behavior that the inspected code does not clearly implement or scope. <br>
Mitigation: Treat cloud upload behavior as unverified until reviewed, and use least-privilege Feishu credentials if upload support is added or enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rfdiosuao/feishu-video-editor) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [skill.json](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration] <br>
**Output Format:** [Markdown status messages and JSON result objects that point to generated video, audio, or SRT subtitle files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local FFmpeg and Python video-processing dependencies; output paths are controlled by the skill configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
