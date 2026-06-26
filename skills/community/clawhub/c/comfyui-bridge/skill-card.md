## Description: <br>
Generate images, faceswap, edit photos, animate expressions, and do style transfer via a self-hosted ComfyUI instance on your LAN. Your GPU, your models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bortlesboat](https://clawhub.ai/user/Bortlesboat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to route image generation, photo editing, face swapping, expression animation, and style transfer tasks to a self-hosted ComfyUI environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images may be sent to the configured bridge and queued as local copies under ~/.openclaw/faceswap-queue. <br>
Mitigation: Review the bridge target before use and define a cleanup process for queued private images. <br>
Risk: Queued results can be sent later through iMessage to a hard-coded default chat target. <br>
Mitigation: Do not run the queue daemon until the chat target and recipient behavior have been checked or changed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Bortlesboat/comfyui-bridge) <br>
- [ComfyUI Bridge Repository](https://github.com/Bortlesboat/comfyui-bridge) <br>
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) <br>
- [Ollama](https://ollama.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local image output paths and may queue requests for later delivery when the bridge is unavailable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
