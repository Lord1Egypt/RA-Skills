## Description: <br>
FMT肠菌移植科普视频制作工具（视频合成+字幕+SRT+配音TTS+片头片尾）。将静态图片/动态视频素材合成为完整科普视频，支持中文字幕、旁白配音、片头片尾合成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, medical communicators, and agents assisting FMT education workflows use this skill to assemble static images, generated clips, SRT subtitles, TTS narration, and ffmpeg commands into Chinese FMT explainer videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package-manager commands may change the user's system environment when ffmpeg is unavailable. <br>
Mitigation: Require explicit user approval before running apt-get or other package-manager commands. <br>
Risk: Video and subtitle composition can overwrite or process unintended files if paths are wrong. <br>
Mitigation: Review all file paths before running ffmpeg, Python, or media-generation commands. <br>
Risk: Narration text sent to TTS or video-generation tools may contain sensitive information. <br>
Mitigation: Avoid submitting sensitive narration text or private media content to generation tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmy1006-sudo/fmt-video-production) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JavaScript, Python, bash, and SRT examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces video-production instructions and file-path conventions for MP4, MP3, SRT, and related media outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
