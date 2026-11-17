## Description:

Generate AI images with 50+ models through the inference.sh CLI, including text-to-image, image editing, inpainting, upscaling, LoRA, and text rendering workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to generate or edit images, create product mockups, produce concept art, upscale media, and test image models through inference.sh CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and image URLs may be sent to inference.sh or model providers during image generation and editing.

Mitigation: Avoid submitting confidential media, proprietary prompts, or regulated data unless the destination service and use case are approved.

Risk: Related-skill examples use unpinned npx install commands.

Mitigation: Verify the source, version, and trust boundary before running or copying related-skill installation commands.

Risk: The security verdict is suspicious due to external data handling and install-command concerns.

Mitigation: Review the skill and its CLI commands before deployment, and require operator approval for external image or prompt workflows.

## Reference(s):

- [Ai Image Gen Pro on ClawHub](https://clawhub.ai/bingze00000/skills/ai-image-gen-pro)
- [inference.sh](https://inference.sh)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Image Generation Example](https://inference.sh/docs/examples/image-generation)
- [Apps Overview](https://inference.sh/docs/apps/overview)
- [inference.sh CLI Install Instructions](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inference.sh CLI commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the infsh CLI and an authenticated inference.sh session.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
