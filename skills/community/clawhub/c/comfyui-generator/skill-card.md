## Description:

Generate AI images and perform style transfers through a ComfyUI integration with batch processing and workflow setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nl108](https://clawhub.ai/user/nl108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect OpenClaw-style workflows to ComfyUI for text-to-image generation, style transfer, prompt optimization, batch jobs, and workflow configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented default API key is reusable and the default endpoint uses HTTP.

Mitigation: Use a trusted local ComfyUI server or an HTTPS endpoint, and replace the default API key with a unique secret before use.

Risk: Local images can be sent to the configured ComfyUI server.

Mitigation: Avoid sending private images unless the configured server is trusted and its handling of uploaded files is understood.

Risk: The skill describes file monitoring and archiving behavior without complete operational detail.

Mitigation: Ask the publisher to document monitoring and archiving behavior before enabling those features.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nl108/skills/comfyui-generator)
- [Publisher profile](https://clawhub.ai/user/nl108)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, Python examples, environment variables, and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local workflow JSON files, image paths, ComfyUI endpoints, and prompt-generation options.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
