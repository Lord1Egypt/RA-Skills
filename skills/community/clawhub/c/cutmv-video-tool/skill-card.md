## Description: <br>
A video processing skill for OpenClaw that uses FFmpeg to cut, convert, compress, inspect, watermark, subtitle, and extract video or audio assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QiaoTuCodes](https://clawhub.ai/user/QiaoTuCodes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to prepare media files for workflows such as messaging-size compression, segment extraction, format conversion, screenshot extraction, audio replacement, watermarking, and subtitle embedding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted media metadata, subtitle files, or FFmpeg filter inputs could trigger unsafe behavior. <br>
Mitigation: Review before installing and avoid untrusted media or subtitle/style inputs until unsafe evaluation is removed and FFmpeg filter values are escaped. <br>
Risk: Video processing commands may overwrite existing output files unexpectedly. <br>
Mitigation: Require explicit confirmation before overwriting files and choose output paths that do not replace important assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QiaoTuCodes/cutmv-video-tool) <br>
- [QiaoTuCodes publisher profile](https://clawhub.ai/user/QiaoTuCodes) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Code] <br>
**Output Format:** [Processed media files with JSON status objects and Python or CLI invocation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FFmpeg and ffprobe on PATH; media operations may overwrite existing output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
