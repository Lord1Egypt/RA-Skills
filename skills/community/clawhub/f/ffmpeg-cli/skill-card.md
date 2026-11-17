## Description:

Process video and audio using FFmpeg CLI for transcoding, cutting, merging, audio extraction, thumbnails, GIFs, speed changes, filters, subtitles, and watermarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ascendswang](https://clawhub.ai/user/ascendswang)

### License/Terms of Use:


## Use Case:

Developers and media operators use this skill to process local audio and video files for conversion, trimming, merging, audio extraction, thumbnail and GIF creation, speed adjustment, and watermarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled FFmpeg helpers can overwrite output files without confirmation.

Mitigation: Use deliberate output filenames, avoid paths that point to valuable existing files, and work on copies when processing important media.

Risk: Untrusted filenames, output paths, playback rates, or watermark positions may be unsafe unless the scripts are hardened first.

Mitigation: Use trusted media paths and validated parameter values; review and harden the scripts before allowing an agent to choose these inputs automatically.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg to be installed in the execution environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
