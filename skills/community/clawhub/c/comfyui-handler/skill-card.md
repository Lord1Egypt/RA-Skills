## Description:

Connects agents to ComfyUI through a Python CLI for prompt-driven image generation and image editing with bundled template workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1878212](https://clawhub.ai/user/1878212)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or edit images by submitting prompts and optional input files to a configured ComfyUI instance through reusable workflow templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a configured ComfyUI service and network path for uploads, prompt execution, polling, and downloads.

Mitigation: Install only when the ComfyUI host and network path are trusted, and keep the host local or behind a trusted encrypted and authenticated channel.

Risk: Sensitive input media may be sent to the configured ComfyUI host, and generated downloads should not be treated as inherently trustworthy.

Mitigation: Avoid sending sensitive images and review generated downloads before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1878212/skills/comfyui-handler)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [JSON status with generated file paths, plus generated media files saved to the workspace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted configured ComfyUI host; supports text-to-image and image-edit workflow templates with portrait or landscape orientation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
