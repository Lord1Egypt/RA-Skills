## Description:

Generate images and videos via ComfyUI on local GPU. Supports Flux text-to-image, Wan2.1 text-to-video, and image-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative technologists use this skill to generate local Flux images and Wan2.1 text-to-video or image-to-video outputs through an existing ComfyUI GPU server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote or malicious ComfyUI endpoints could receive prompts, input images, or workflow data.

Mitigation: Use only a trusted local ComfyUI server and avoid setting COMFYUI_URL or --url to remote hosts.

Risk: Input image handling may copy sensitive files into the ComfyUI input directory.

Mitigation: Do not process sensitive source images unless that local copy behavior is acceptable.

Risk: Unsafe file path handling could expose local files or write outputs outside expected locations.

Mitigation: Run under an unprivileged account, use cautious input and output paths, and add filename containment checks before broader deployment.

Risk: Unpinned dependencies or model downloads can change over time.

Mitigation: Prefer pinned commits and verified model checksums during installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/skills/comfyui-image-video)
- [ComfyUI repository](https://github.com/comfyanonymous/ComfyUI.git)
- [ComfyUI and Flux model reference](artifact/references/models.md)
- [PyTorch CUDA wheel index](https://download.pytorch.org/whl/cu128)
- [Hugging Face mirror endpoint](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [PNG image files or directories of PNG video frames, with terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local ComfyUI server and installed model assets; video frame sequences may require separate MP4 post-processing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
