## Description: <br>
Generate images, perform style transfer, run batch jobs, and manage ComfyUI workflows through OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nl108](https://clawhub.ai/user/nl108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative automation users can use this skill to connect OpenClaw to a trusted ComfyUI server for image generation, style transfer, prompt optimization, and batch media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a ComfyUI server and can upload images to that endpoint. <br>
Mitigation: Keep COMFY_BASE_URL pointed at localhost or infrastructure you control, and avoid sending sensitive images to untrusted endpoints. <br>
Risk: Separate workflow or monitoring files can alter ComfyUI behavior. <br>
Mitigation: Review workflow and monitoring files before adding them to ComfyUI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nl108/comfyui-generator) <br>
- [Publisher profile](https://clawhub.ai/user/nl108) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit prompts, workflow JSON, and image uploads to the configured ComfyUI endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
