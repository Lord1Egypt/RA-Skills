## Description: <br>
Comprehensive video/audio processing with FFmpeg for transcoding, cutting, merging, audio extraction, thumbnails, GIFs, speed adjustments, filters, subtitles, and watermarks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ascendswang](https://clawhub.ai/user/ascendswang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and media engineers use this skill to generate and run local FFmpeg command workflows for common video and audio processing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The FFmpeg helper scripts can overwrite existing output files. <br>
Mitigation: Use fresh output filenames and review target paths before running generated commands. <br>
Risk: Untrusted filenames or merge file lists can affect local FFmpeg command behavior. <br>
Mitigation: Use only trusted local media files and avoid passing filenames or file lists from untrusted sources, especially to merge.sh. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ascendswang/ffmpeg-cli) <br>
- [Publisher profile](https://clawhub.ai/user/ascendswang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and script usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local FFmpeg workflows that may create or overwrite media files selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
