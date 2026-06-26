## Description: <br>
Generates images locally through ComfyUI and Flux.1 Dev, including optional PuLID face-reference generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisliu95](https://clawhub.ai/user/chrisliu95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate local images, presentation graphics, and face-consistent portraits through a running ComfyUI instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images can be sent to any COMFYUI_URL value, which may expose sensitive content if it points away from a trusted local ComfyUI instance. <br>
Mitigation: Keep COMFYUI_URL pointed at a trusted local ComfyUI instance and avoid sensitive prompts or files. <br>
Risk: PuLID generation handles face-reference images and can create face-consistent outputs. <br>
Mitigation: Use reference face images only with consent and review generated outputs before sharing. <br>
Risk: Downloaded image bytes are written to the default generated-images/ directory or a custom --output path. <br>
Mitigation: Choose output paths deliberately and review file destinations before running the scripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chrisliu95/comfyui-flux) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image files plus MEDIA:<path> text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves generated images to generated-images/ by default or to a user-provided --output path after polling the configured ComfyUI endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
