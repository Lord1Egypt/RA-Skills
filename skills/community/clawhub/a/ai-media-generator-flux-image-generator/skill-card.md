## Description:

Use when someone asks for flux image generator, flux text-to-image, flux prompt examples, flux image model selection, or CLI-based image generation with flux-style models on ricebowl.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinchanzis](https://clawhub.ai/user/jinchanzis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to choose Flux-capable image models on ricebowl.ai and run CLI-based text-to-image generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party npm CLI.

Mitigation: Install the CLI only from a trusted package source and review the package before using it in sensitive environments.

Risk: The workflow uses a ricebowl.ai media-service API key that may consume credits or grant account access.

Mitigation: Use a limited API key when possible, monitor credit usage, and rotate the key if local CLI configuration or the package is suspected to be compromised.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinchanzis/skills/ai-media-generator-flux-image-generator)
- [ai-media-generator homepage](https://github.com/214140846/ai-media-generator)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference ricebowl.ai API-key setup, Flux model selection, image generation, and image retrieval commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
