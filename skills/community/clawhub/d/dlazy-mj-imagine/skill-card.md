## Description:

Midjourney-style image generation with aspect ratio, bot type, and output selection options for artistic, strongly stylized creations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative teams can generate stylized images from prompts, choosing an aspect ratio, Midjourney or Niji Journey bot, and grid or individual output selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial and recommends checking the referenced CLI and its credential handling before installation.

Mitigation: Review the CLI and its credential handling before installing or using it.

Risk: Prompts are sent to dLazy's hosted service, and local media supplied to the CLI may be uploaded for processing.

Mitigation: Avoid sending sensitive prompts or media, and review the service terms before use.

Risk: The skill requires a dLazy API key, which can be stored in the CLI user configuration or supplied through an environment variable.

Mitigation: Protect the key, use environment-specific secrets handling where appropriate, and rotate or revoke it if exposed.

## Reference(s):

- [dLazy CLI project](https://github.com/dlazy-ai/cli)
- [@dlazy/cli package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Images, JSON, API Calls]

**Output Format:** [Generated image URLs or saved image files, with JSON result metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports aspect-ratio and bot selection, grid or individual outputs, and asynchronous task IDs.]

## Skill Version(s):

1.3.43 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
