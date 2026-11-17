## Description:

Canvas Workspace helps agents generate images, edit existing images from canvas selections or marker files, push image URLs into a local canvas workspace, and inspect canvas state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanming1](https://clawhub.ai/user/quanming1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to work with image-generation and image-editing workflows in a canvas workspace, including sending model outputs or existing image URLs to the local canvas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to run mutable external code through an unpinned npm package reference.

Mitigation: Pin and verify the npm package version, and review the package before execution in a restricted environment.

Risk: The skill asks users to persist image provider API keys in shell startup files.

Mitigation: Use a secure secret manager or session-scoped environment variables instead of storing provider API keys in shell profiles.

Risk: Prompts and image URLs may be sent to Qwen, Gemini, or a configured compatible provider.

Mitigation: Do not pass sensitive prompts, local files, private image URLs, or internal URLs unless they are intended to be shared with the selected provider.

Risk: Automatic skill activation can start workflows that make external calls or launch local services.

Mitigation: Keep automatic activation disabled or require explicit user confirmation before running canvas, generation, edit, or push commands.

## Reference(s):

- [Canvas API Reference](artifact/references/canvas-api.md)
- [Canvas Workspace on ClawHub](https://clawhub.ai/quanming1/skills/canvas-workspace)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local canvas API calls and image provider scripts that return JSON containing image URLs, local canvas URLs, element IDs, and push status.]

## Skill Version(s):

1.4.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
