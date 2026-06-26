## Description: <br>
Generate images and videos via ComfyUI on local GPU. Supports Flux text-to-image, Wan2.1 text-to-video, and image-to-video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate local GPU images and short video frame sequences through a ComfyUI server. It supports text-to-image, text-to-video, and image-to-video workflows with configurable prompts, sizes, seeds, model names, and output paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing the ComfyUI URL to a remote server can send prompts and image-to-video input images to that server. <br>
Mitigation: Keep COMFYUI_URL on 127.0.0.1 unless the remote server is explicitly trusted. <br>
Risk: Large model downloads, GPU workloads, and a user-level background service can consume significant local resources. <br>
Mitigation: Install only on an intended local GPU host, review model sources, and monitor disk, GPU memory, and service configuration. <br>


## Reference(s): <br>
- [ComfyUI Image & Video Generation on ClawHub](https://clawhub.ai/vincentlau2046-sudo/comfyui-image-video) <br>
- [ComfyUI + Flux model reference](references/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Generated PNG images or PNG frame sequences with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, a local ComfyUI service, local model files, and sufficient GPU memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
