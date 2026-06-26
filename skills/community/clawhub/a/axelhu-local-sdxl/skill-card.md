## Description: <br>
Generates private SDXL images through a local ComfyUI instance with configurable prompts, dimensions, sampler, steps, seed, and CFG. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate local images for privacy-sensitive, commercial-material, or online-rate-limited workflows when the user explicitly requests local or private image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated images may leave the local environment if the agent sends them through Feishu or chat delivery paths. <br>
Mitigation: For sensitive or commercial images, request local-save-only handling and require explicit approval before sharing generated files outside the local machine. <br>
Risk: Large dimensions or high step counts can exceed local GPU capacity or make generation unreliable. <br>
Mitigation: Keep dimensions and sampling steps within the documented RTX 3080 limits, and reduce resolution or steps when generation fails or slows significantly. <br>
Risk: The skill depends on the user's local ComfyUI and SDXL model setup. <br>
Mitigation: Install only when the local ComfyUI and model files are trusted, and run ComfyUI bound to 127.0.0.1 as documented. <br>


## Reference(s): <br>
- [Deployment Guide](references/deployment.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/axelhu/axelhu-local-sdxl) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image files with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves output to a requested path or /tmp and calls a local ComfyUI service on localhost:8188.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
