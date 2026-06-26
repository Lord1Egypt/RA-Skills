## Description: <br>
Run local ComfyUI workflows via the HTTP API. Use when the user asks to run ComfyUI, execute a workflow by file path/name, or supply raw API-format JSON; supports the default workflow bundled in assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelvincai522](https://clawhub.ai/user/kelvincai522) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and image-generation users use this skill to edit ComfyUI workflow JSON, queue workflows on a local ComfyUI server, download model weights, and return generated image outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run pget to download model files. <br>
Mitigation: Use --no-pget or install pget yourself from a verified source before using model downloads. <br>
Risk: User-supplied model URLs can persist downloaded files under the local ComfyUI models directory. <br>
Mitigation: Use trusted model URLs, verify hashes when available, and avoid --overwrite for untrusted files. <br>
Risk: Workflow JSON is submitted to a local ComfyUI server for execution. <br>
Mitigation: Review workflow JSON before running it and use the local server intentionally. <br>


## Reference(s): <br>
- [ClawHub ComfyUI skill page](https://clawhub.ai/kelvincai522/comfyui) <br>
- [ComfyUI repository](https://github.com/comfyanonymous/ComfyUI.git) <br>
- [pget download helper](https://github.com/replicate/pget) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON, API calls, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, edited workflow JSON, API responses, and generated image file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write temporary workflow JSON, download model files under the local ComfyUI models directory, and return generated images from ComfyUI output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
