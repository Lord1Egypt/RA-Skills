## Description:

Generates and transforms images by selecting a suitable dLazy CLI model for the prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or edit images from prompts and reference media, choosing among the listed dLazy image models and related image tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes a mismatch between the image-generation description and additional video and speech workflows, and reports incomplete scan coverage.

Mitigation: Review the skill instructions and CLI behavior, including any video or speech commands, before installation or use.

Risk: Using the hosted service requires a dLazy API key, and the skill describes sending prompts and supplied media to dLazy services.

Mitigation: Review the CLI installation and API-key requirements and ensure prompts and media are appropriate to send to the hosted service.

## Reference(s):

- [dLazy website](https://dlazy.com)
- [CLI repository listed in skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-image-generate)

## Skill Output:

**Output Type(s):** [Images, SVG graphics, Image URLs, JSON]

**Output Format:** [Generated image or SVG assets returned as hosted URLs in a JSON response envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The selected model determines image format, resolution, and whether reference media is used.]

## Skill Version(s):

1.3.42 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
