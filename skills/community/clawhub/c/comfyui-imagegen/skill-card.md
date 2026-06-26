## Description: <br>
Generate images via ComfyUI API (localhost:8188) using Flux2 workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halr9000](https://clawhub.ai/user/halr9000) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to turn structured image requests into ComfyUI Flux2 jobs, submit them to a trusted ComfyUI server, and retrieve generated JPG images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The async workflow can send generated images to a hard-coded Telegram recipient. <br>
Mitigation: Review and edit the async command before use; remove or replace the Telegram target unless that exact recipient is intended. <br>
Risk: The async workflow can delete local generated image copies after sending. <br>
Mitigation: Remove automatic deletion when local retention or auditability is required. <br>
Risk: The script can submit prompts to any configured ComfyUI host. <br>
Mitigation: Keep --host pointed at a trusted ComfyUI server and review remote host settings before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/halr9000/comfyui-imagegen) <br>
- [Black Forest Labs Flux2 Klein prompting guide](https://docs.bfl.ml/guides/prompting_guide_flux2_klein) <br>
- [fal.ai Flux 2 Klein prompt guide](https://fal.ai/learn/devs/flux-2-klein-prompt-guide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON prompt examples and shell commands; generated image files are produced by the ComfyUI workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports structured JSON prompts, seed and step customization, submit-only mode, and watch/download mode.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and SKILL.md changelog, released 2026-02-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
