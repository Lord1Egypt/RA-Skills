## Description:

Remove watermarks from videos using ffmpeg delogo filter for fixed-position or dynamically moving overlays while noting that transparent or complex AI-generated watermarks require a different pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ozzylennon](https://clawhub.ai/user/ozzylennon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to remove visible logo, text, or watermark overlays from videos by locating the overlay in sample frames and applying FFmpeg delogo processing. It supports a single fixed region or segmented processing when the watermark moves between distinct positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video-processing helper scripts use predictable or reusable temporary paths that could overwrite local files in some environments.

Mitigation: Run the skill in a contained workspace or under an unprivileged account, and update the helpers to use private unpredictable temporary directories with no preexisting-path reuse before broader deployment.

Risk: The skill uses FFmpeg delogo, which blurs or averages the selected region and may leave traces on transparent, complex, or textured watermarks.

Mitigation: Verify output frames before delivery and route unsuitable cases to a content-aware inpainting workflow when delogo quality is insufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ozzylennon/skills/ffmpeg-video-watermark-remover)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional generated video-processing files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce extracted sample frames and processed video files through FFmpeg helper scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
