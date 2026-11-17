## Description:

Generate 3D rendered art and icons. Use when the user asks for 3D graphics, claymorphism, octane render, or blender 3d style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to generate 3D-styled images, rendered icons, and image variations through a WeryAI image-generation gateway. It supports text-to-image, image-to-image, batch generation, style presets, and local project configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags review-worthy API-key handling concerns.

Mitigation: Use a limited or disposable WeryAI API key, prefer environment injection, and avoid persisting the key unless the user explicitly approves.

Risk: The security summary flags local file upload concerns for reference-image workflows.

Mitigation: Use public HTTPS reference URLs when possible, and only pass local reference files when the user intends to upload their full contents.

Risk: The security summary flags under-disclosed runtime installation behavior.

Mitigation: Require the agent to disclose exact install commands before adding runtime tooling globally.

Risk: The skill relies on a remote image-generation gateway and downloaded result URLs.

Mitigation: Review generated content before use and verify downloaded files are complete before depending on them in downstream workflows.

## Reference(s):

- [WeryAI gateway alignment notes](references/weryai-platform.md)
- [Style presets](references/style-presets.md)
- [First-time setup](references/config/first-time-setup.md)
- [Model registry schema](references/config/model-registry-schema.md)
- [Preferences schema](references/config/preferences-schema.md)
- [WeryAI API keys](https://weryai.com/api/keys)
- [WeryAI API history](https://weryai.com/api/history)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image files, JSON status summaries, and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMAGE_GEN_API_KEY and local Node/npm plus bun or npx runtime tooling; generated images may be downloaded from gateway-provided URLs.]

## Skill Version(s):

2026.3.23 (source: server release metadata; artifact frontmatter reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
