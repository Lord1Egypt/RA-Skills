## Description:

Generate chalkboard art and chalk drawings when the user asks for chalk art, a blackboard menu, or pastel drawing on a dark background.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate chalkboard-style images, menus, illustrations, and batch image sets through a WeryAI image gateway. It helps an agent assemble prompts, select or initialize an image model, run text-to-image or image-to-image jobs, and deliver the generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a remote WeryAI image gateway and transmits generation requests, prompts, and approved reference images to that service.

Mitigation: Use only prompts and reference images that are acceptable to send to the remote gateway, and review the selected model and gateway behavior before production use.

Risk: The skill requires IMAGE_GEN_API_KEY and can persist the key in a project or home .env file when setup is approved.

Mitigation: Store API keys only in approved local secret locations, avoid echoing keys in chat or logs, and review setup commands before allowing persistence.

Risk: The server security summary flags under-disclosed local file, credential, installation, and configuration behaviors.

Mitigation: Ask to see exact install and setup commands before approving runtime setup, and verify any local reference-image path before upload.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/632657122/skills/chalk-art-image-generator)
- [Gateway Alignment Notes](references/weryai-platform.md)
- [First-Time Setup](references/config/first-time-setup.md)
- [Model Registry Schema](references/config/model-registry-schema.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Style Presets](references/style-presets.md)
- [WeryAI API Keys](https://weryai.com/api/keys)
- [WeryAI API History](https://weryai.com/api/history)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated image file or URL outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated image files and project or home configuration under .image-skills/chalk-art-image-generator/.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
