## Description:

A multi-functional audio generation tool for SFX generation, video-to-audio and text-to-audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjx-research](https://clawhub.ai/user/yjx-research)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate sound effects, background audio, or Foley-style audio from text prompts, video files, and optional reference audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user media to a remote ControlFoley service for processing.

Mitigation: Use only non-sensitive media and validate behavior with a small test clip before broader use.

Risk: The release security summary reports flaws that can expose local files or fetch untrusted URLs during normal use.

Mitigation: Review before installing, avoid prompt, model, or negative values beginning with @ or <, and prefer a patched version with native multipart upload, download URL validation, and size limits.

Risk: Returned downloads come from service-provided URLs.

Mitigation: Treat generated downloads as untrusted files and inspect them before using them in downstream workflows.

## Reference(s):

- [ControlFoley Audio Generator API Reference](references/api-reference.md)
- [ControlFoley project page](https://yjx-research.github.io/ControlFoley_web_page/)
- [ControlFoley online demo](https://yjx-research.github.io/ControlFoley_web_page/#try-gen)
- [ControlFoley model weights](https://huggingface.co/YJX-Xiaomi/ControlFoley/)
- [ControlFoley source repository](https://github.com/xiaomi-research/controlfoley)

## Skill Output:

**Output Type(s):** [Files, Shell commands, API Calls, Guidance]

**Output Format:** [Generated audio/video files with text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces FLAC audio and, for video-to-audio workflows, MP4 video with generated audio.]

## Skill Version(s):

1.0.9 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
