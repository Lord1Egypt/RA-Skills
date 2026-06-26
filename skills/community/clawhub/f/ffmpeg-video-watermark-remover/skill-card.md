## Description: <br>
Removes fixed or segmented moving video watermarks by helping an agent identify delogo regions, run FFmpeg processing commands, and verify the edited result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ozzylennon](https://clawhub.ai/user/ozzylennon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and agents use this skill to process videos they own or are authorized to edit by locating watermark regions and applying FFmpeg delogo filters. It supports fixed-position watermarks and segmented processing for watermarks that move between distinct positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watermark removal can be misused to remove third-party attribution, creator marks, platform watermarks, or provenance indicators. <br>
Mitigation: Install and use only for videos the user owns or is clearly authorized to edit; do not use it to remove third-party attribution or provenance marks. <br>
Risk: The helper scripts and FFmpeg examples use overwrite behavior, so careless output paths can replace existing files. <br>
Mitigation: Use unique output paths, review destination filenames before execution, and keep backups of source media. <br>
Risk: The FFmpeg delogo filter fills regions with blurred or averaged pixels and may leave visible traces on complex, transparent, or textured watermarks. <br>
Mitigation: Inspect sample frames and verify the output before delivery; use a different inpainting workflow when delogo quality is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ozzylennon/ffmpeg-video-watermark-remover) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce edited video files, sample frames, temporary segment files, and concat manifests when executed by an agent with FFmpeg available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
