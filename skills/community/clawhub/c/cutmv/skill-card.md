## Description: <br>
cutmv is a local FFmpeg-based video processing skill for cutting media, converting formats, compressing videos, extracting frames or audio, replacing or mixing audio, and adding text watermarks or subtitles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QiaoTuCodes](https://clawhub.ai/user/QiaoTuCodes) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and agents use this skill to perform common local video and audio transformations through a Python API or CLI, especially preparing media for size limits, format compatibility, screenshots, audio track edits, watermarks, and subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The info command evaluates media metadata as Python code. <br>
Mitigation: Review or patch the eval() call before installation, and avoid running the info command on untrusted media. <br>
Risk: FFmpeg commands use overwrite behavior for output paths. <br>
Mitigation: Choose output paths carefully and avoid pointing commands at files that must be preserved. <br>
Risk: The skill depends on the system FFmpeg and ffprobe binaries. <br>
Mitigation: Use a trusted local FFmpeg/ffprobe installation from a known source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QiaoTuCodes/cutmv) <br>
- [Publisher profile](https://clawhub.ai/user/QiaoTuCodes) <br>
- [FFmpeg](https://ffmpeg.org/) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime commands return JSON-like status dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local FFmpeg/ffprobe installation and read/write access to media input and output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
