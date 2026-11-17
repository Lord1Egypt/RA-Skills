## Description:

Generates local SDXL images through a ComfyUI setup for private or explicitly local image-generation requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate high-quality images locally with SDXL when they explicitly request private, local, or offline image generation instead of an online image service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated images may be stored on the local ComfyUI host.

Mitigation: Use trusted local environments and verify storage paths before processing sensitive prompts or private images.

Risk: The documentation claims Feishu delivery, while security evidence says the included script does not implement that behavior.

Mitigation: Confirm any surrounding agent integration before using sensitive images or relying on Feishu delivery.

## Reference(s):

- [Deployment guide](artifact/references/deployment.md)
- [ClawHub skill page](https://clawhub.ai/axelhu/skills/axelhu-local-sdxl)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG image files with terminal status text and an output path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local ComfyUI service on localhost:8188 and an SDXL checkpoint.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
