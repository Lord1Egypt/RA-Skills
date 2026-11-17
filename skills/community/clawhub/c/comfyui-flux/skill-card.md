## Description:

Generates local images through ComfyUI with Flux.1 Dev, including standard prompt-based generation and optional PuLID face-consistent generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisliu95](https://clawhub.ai/user/chrisliu95)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run local ComfyUI image generation for prompt-based images and presentation graphics, and to optionally produce face-consistent images when a trusted local ComfyUI/PuLID setup is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts or reference face images can be sent to an arbitrary ComfyUI endpoint if COMFYUI_URL is changed.

Mitigation: Use only a trusted loopback ComfyUI endpoint and check COMFYUI_URL before running the scripts.

Risk: Face-consistent generation uploads reference face images to the configured ComfyUI server for processing.

Mitigation: Provide face reference images only when the user is comfortable with how that ComfyUI server stores and processes them.

Risk: The security scan verdict is suspicious because face-image handling is under-scoped and endpoint trust is configurable.

Mitigation: Review the skill before installing and prefer tightening default endpoint guidance to loopback-only operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrisliu95/skills/comfyui-flux)
- [Publisher profile](https://clawhub.ai/user/chrisliu95)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown instructions with shell commands; generated image files reported as MEDIA:<path>]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable trusted ComfyUI endpoint; generated images are saved under generated-images/ or a user-specified path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
