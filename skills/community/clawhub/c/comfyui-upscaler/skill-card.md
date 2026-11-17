## Description:

帮助 ComfyUI 用户生成三重放大工作流，用于放大 AI 生成图片、小图和高清图像，并提升分辨率、细节和清晰度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmin1113](https://clawhub.ai/user/jmin1113)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, artists, and ComfyUI users use this skill to generate and load workflow JSON for multi-stage image upscaling. It supports text-to-image and image-to-image workflows that combine latent-space resampling, tiled upscaling, and model-based sharpening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unspecified ComfyUI nodes or similarly named models from unverified sources can introduce unsafe or incorrect components.

Mitigation: Review required nodes and models before installing; prefer pinned repositories, known publishers, checksums, and isolated non-admin ComfyUI environments.

Risk: High-resolution upscaling workflows can fail on limited GPU memory or produce seams, distortion, or blurry output when parameters are too aggressive.

Mitigation: Adjust tile size, denoise strength, seam settings, and upscale factor according to available VRAM and image type before running large jobs.

## Reference(s):

- [工作流详解](references/workflow_details.md)
- [模型推荐](references/models.md)
- [常见问题](references/faq.md)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [4x Faces Sharp model reference](https://huggingface.co/FacehugmanIII/4x_faces_Sharp_Better_higher_quality)
- [CivitAI models](https://civitai.com/models)
- [OpenModelDB](https://openmodeldb.info/)
- [ClawHub skill page](https://clawhub.ai/jmin1113/skills/comfyui-upscaler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated ComfyUI workflow JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ComfyUI workflow configuration for user-selected base models, upscale models, tile size, scale, denoise strength, and output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
