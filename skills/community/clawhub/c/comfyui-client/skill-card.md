## Description:

Automates ComfyUI image and video generation by loading workflow JSON, updating prompts and image inputs, queueing jobs, polling completion, and downloading generated media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imjszhang](https://clawhub.ai/user/imjszhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to run bundled or supplied ComfyUI workflows for text-to-image, image editing, ControlNet-guided redraws, image-to-video, and first/last-frame video generation. It is useful when an agent needs to configure a workflow, submit it to a reachable ComfyUI server, and collect generated media outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured ComfyUI server can influence downloaded output filenames, and a malicious or compromised server may cause files to be created or overwritten outside the intended output folder.

Mitigation: Use the skill only with a trusted local ComfyUI server or a server you control; avoid untrusted values for --server or COMFYUI_SERVER_URL.

Risk: Using --image-path uploads local image files to the configured ComfyUI server.

Mitigation: Upload only files intended for that server and avoid sending sensitive local images to remote or shared ComfyUI instances.

Risk: Generated prompts, workflows, result metadata, and media are saved locally by default.

Mitigation: Review the configured output directory and clean or protect generated session folders according to the sensitivity of the prompts and media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imjszhang/skills/comfyui-client)
- [Workflow paths reference](artifact/references/workflow_paths.md)
- [ComfyUI subgraph documentation](https://docs.comfy.org/interface/features/subgraph)
- [ComfyUI workflow template issues](https://github.com/Comfy-Org/workflow_templates/issues)
- [Z-Image Turbo diffusion model](https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors)
- [Z-Image Turbo ControlNet Union model](https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union/resolve/main/Z-Image-Turbo-Fun-Controlnet-Union.safetensors)
- [Qwen Image ComfyUI VAE](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors)
- [Wan text encoder](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors)
- [HunyuanVideo Qwen text encoder](https://huggingface.co/Comfy-Org/HunyuanVideo_1.5_repackaged/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples and JSON workflow inputs; script execution writes session JSON plus generated image or video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable ComfyUI server and installed model dependencies for the selected workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
