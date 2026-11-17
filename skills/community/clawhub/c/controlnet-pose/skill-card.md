## Description:

Pose-conditioned generation on RunComfy via the runcomfy CLI, routing video motion transfer and still-image pose conditioning requests across Kling Motion Control, Wan Animate, and Z-Image ControlNet LoRA endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to choose and invoke RunComfy routes for pose-conditioned image generation, motion transfer, and character animation from user-provided reference media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RunComfy CLI package may be installed from npm without a pinned version.

Mitigation: Use a pinned, verified @runcomfy/cli version and avoid arbitrary remote install scripts.

Risk: Prompts, reference media, and control images are sent to RunComfy's cloud service.

Mitigation: Only provide media URLs and prompts intended for RunComfy processing, and use a least-privileged RUNCOMFY_TOKEN where possible.

Risk: Untrusted third-party reference media can influence generated outputs.

Mitigation: Use user-provided reference URLs and review generated outputs for divergence from the prompt.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/controlnet-pose)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose)
- [Kling 2.6 Motion Control Pro](https://www.runcomfy.com/models/kling/kling-2-6/motion-control-pro?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose)
- [Kling 2.6 Motion Control Standard](https://www.runcomfy.com/models/kling/kling-2-6/motion-control-standard?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose)
- [Wan 2.2 Animate video-to-video](https://www.runcomfy.com/models/community/wan-2-2-animate/video-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose)
- [Z-Image Turbo ControlNet LoRA](https://www.runcomfy.com/models/tongyi-mai/z-image/turbo/controlnet/lora?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose)
- [Mastering ControlNet in ComfyUI](https://www.runcomfy.com/tutorials/mastering-controlnet-in-comfyui?utm_source=clawhub&utm_medium=skill&utm_campaign=controlnet-pose)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces RunComfy CLI route recommendations and command examples; generated media is downloaded by the CLI to the requested output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
