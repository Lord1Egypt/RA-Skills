## Description: <br>
Automates ComfyUI image and video generation by loading workflows, updating prompts and image nodes, submitting jobs, polling results, and downloading generated media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imjszhang](https://clawhub.ai/user/imjszhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run ComfyUI workflows for text-to-image, image editing, image-to-video, and batch media generation tasks when a ComfyUI server and required models are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, input images, and generated media may be sent to the configured ComfyUI server. <br>
Mitigation: Keep the server URL local or otherwise trusted, and avoid uploading sensitive images to remote ComfyUI servers. <br>
Risk: Generated media, prompts, and workflow details are saved in the output directory. <br>
Mitigation: Clean the output directory when generated media or prompts should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imjszhang/comfyui-client) <br>
- [Workflow path reference](artifact/references/workflow_paths.md) <br>
- [ComfyUI subgraph documentation](https://docs.comfy.org/interface/features/subgraph) <br>
- [ComfyUI workflow template issues](https://github.com/Comfy-Org/workflow_templates/issues) <br>
- [Z-Image Turbo model assets](https://huggingface.co/Comfy-Org/z_image_turbo) <br>
- [Qwen-Image ComfyUI model assets](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI) <br>
- [Wan 2.1 ComfyUI repackaged model assets](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and generated media/session files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes session_info.json, workflow.json, result.json, error.json, and downloaded image or video files under work_dir/comfyui_output/<session>.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
