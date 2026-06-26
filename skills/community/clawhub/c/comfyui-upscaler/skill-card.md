## Description: <br>
Generates ComfyUI workflow JSON for triple-stage image upscaling, with local environment checks and guidance for base models, upscaling models, tile size, scale, denoise, and output path settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmin1113](https://clawhub.ai/user/jmin1113) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ComfyUI users use this skill to check a local ComfyUI setup and generate importable upscaling workflows for AI-generated or low-resolution images. It supports text-to-image and image-to-image workflows that combine latent-space resampling, tiled upscaling, and model-based sharpening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow generator writes a local JSON file to the user-provided output path. <br>
Mitigation: Review the output path before running the generator so workflow files are written only where intended. <br>
Risk: The skill recommends downloading ComfyUI models from external model sources. <br>
Mitigation: Download recommended models only from sources you trust and confirm their terms before use. <br>
Risk: Large tile sizes, high scale values, or aggressive denoise settings can exceed available VRAM or distort the image. <br>
Mitigation: Use the FAQ guidance to lower tile size, scale, or denoise when memory errors or visual artifacts occur. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jmin1113/comfyui-upscaler) <br>
- [Workflow details](references/workflow_details.md) <br>
- [Recommended models](references/models.md) <br>
- [FAQ](references/faq.md) <br>
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) <br>
- [4x Faces Sharp model](https://huggingface.co/FacehugmanIII/4x_faces_Sharp_Better_higher_quality) <br>
- [CivitAI models](https://civitai.com/models) <br>
- [OpenModelDB](https://openmodeldb.info/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files] <br>
**Output Format:** [Markdown guidance with bash commands and ComfyUI workflow JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local ComfyUI workflow JSON to the requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
