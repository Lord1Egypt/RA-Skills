## Description: <br>
Extract frames or short clips from videos using ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agents working with local video files use this skill to extract a first frame or a timestamped/indexed frame for quick inspection, thumbnail generation, or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper overwrites the selected output path. <br>
Mitigation: Use explicit scratch or newly named output paths, and avoid pointing --out at important existing files. <br>
Risk: The workflow depends on a local ffmpeg installation. <br>
Mitigation: Install ffmpeg from a trusted package source such as the Homebrew formula listed in the skill metadata. <br>


## Reference(s): <br>
- [Dalong Video Frames on ClawHub](https://clawhub.ai/1yihui/dalong-video-frames) <br>
- [FFmpeg](https://ffmpeg.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one extracted frame to the requested output path; the helper uses ffmpeg overwrite behavior for the chosen destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
