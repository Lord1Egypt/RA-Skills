## Description:

Generate images using Black Forest Labs FLUX.2-pro via Azure AI Foundry, with support for custom dimensions, reproducible seeds, and optional Chinese text overlay through Node.js Canvas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zwcih](https://clawhub.ai/user/zwcih)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative agents use this skill to produce image files from text prompts through a configured FLUX.2-pro Azure AI Foundry endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to the configured FLUX/Azure endpoint and may contain sensitive information.

Mitigation: Do not include secrets, private data, or regulated information in prompts.

Risk: The script sends FLUX_API_KEY to the URL stored in FLUX_ENDPOINT.

Mitigation: Set FLUX_ENDPOINT only to a trusted Azure AI Foundry endpoint before running the skill.

Risk: The optional Canvas overlay path can add npm dependency exposure.

Mitigation: Pin optional npm dependencies when using Canvas-based text overlay.

## Reference(s):

- [Azure AI Foundry FLUX API Reference](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/zwcih/skills/azure-flux-image-gen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JavaScript examples; the bundled script writes PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image output depends on FLUX_ENDPOINT, FLUX_API_KEY, prompt, width, height, output path, and optional seed.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
