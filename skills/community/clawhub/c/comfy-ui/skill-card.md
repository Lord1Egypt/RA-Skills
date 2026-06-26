## Description: <br>
Generate high-quality images through a local ComfyUI instance for private image generation on user-controlled hardware and custom workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dihan](https://clawhub.ai/user/dihan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate images through a ComfyUI server they control, including custom workflow JSON files when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using an untrusted ComfyUI endpoint can expose prompts, workflows, or generated outputs outside the user's controlled environment. <br>
Mitigation: Configure the skill only with a ComfyUI server you control, and avoid third-party endpoints. <br>
Risk: Workflow and file handling are broader than the documentation bounds. <br>
Mitigation: Do not pass sensitive JSON files as workflows; review workflow paths and sanitize downloaded filenames before broad use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dihan/comfy-ui) <br>
- [Publisher profile](https://clawhub.ai/user/dihan) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; the helper script returns a local generated image path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COMFYUI_SERVER_ADDRESS and a running ComfyUI server; optional workflow JSON can be supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
