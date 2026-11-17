## Description:

Use DMXAPI to generate and edit images with models including Gemini, Seedream, and OpenAI, supporting text-to-image, image editing, multi-image fusion, and web-search-enhanced image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onee-io](https://clawhub.ai/user/onee-io)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and run DMXAPI CLI commands for image generation, image editing, multi-image fusion, and web-search-enhanced image creation, then report where generated images are saved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external dmxapi-cli package and DMXAPI service.

Mitigation: Install only if you trust DMXAPI and dmxapi-cli; prefer a pinned or local CLI install where possible.

Risk: DMXAPI API keys could be exposed or overused if broadly scoped or long lived.

Mitigation: Use a limited, revocable API key and avoid sharing it in prompts, logs, or generated output.

Risk: Prompts and source images may be sent to external model providers through DMXAPI.

Mitigation: Avoid sending sensitive prompts or private images unless that data sharing is acceptable.

## Reference(s):

- [DMXAPI Console](https://www.dmxapi.cn/)
- [ClawHub skill page](https://clawhub.ai/onee-io/skills/dmxapi-image-generation)
- [Publisher profile](https://clawhub.ai/user/onee-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and saved image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20+, dmxapi-cli, a configured DMXAPI API key, and local image paths for image editing or fusion.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
