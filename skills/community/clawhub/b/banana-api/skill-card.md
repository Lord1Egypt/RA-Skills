## Description:

Generate and edit images using Nano Banana (Gemini-3-Pro-Image-Preview) API with automatic base64 handling, image compression, and optional Discord sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonboi](https://clawhub.ai/user/jasonboi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate new images or edit local images through the Nano Banana image API while avoiding manual base64 encoding, decoding, compression, and file handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, input images, and bearer API keys are sent to an under-disclosed hard-coded web endpoint.

Mitigation: Use only with trusted data, avoid private or regulated images, and review trust in nn.147ai.com before installation or execution.

Risk: API keys may be stored in plaintext by the documented config-file workflow.

Mitigation: Prefer environment variables or a secret manager, use a narrow or disposable key where possible, and rotate keys already used with the tool.

Risk: Providing a Discord channel ID allows generated image results to be sent to Discord.

Mitigation: Treat --channel-id as explicit sharing permission and verify the target channel before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonboi/skills/banana-api)
- [Nano Banana API endpoint](https://nn.147ai.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash commands; generated PNG image files from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script prints an OUTPUT_PATH line for workflow integration and can optionally send generated images to Discord.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
