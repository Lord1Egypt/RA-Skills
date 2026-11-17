## Description:

1MP raster image generation with refined design judgment. Suitable for everyday creative work and fast iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users can ask an agent to generate 1MP raster images from prompts, choose an aspect ratio, and save or retrieve the resulting image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the CLI behavior was not assessed, and the authentication setup is not clearly tied to image generation.

Mitigation: Review the CLI package and its authentication behavior before installing or using it.

Risk: The skill says prompts are sent to dLazy and supplied local media files are uploaded to its hosted storage.

Mitigation: Avoid sending confidential prompts or sensitive media, and review the service terms before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-recraft-v4)
- [dLazy CLI package (version 1.2.3 listed in skill metadata)](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Raster images, JSON]

**Output Format:** [Image assets returned through hosted URLs in a JSON response; images can also be saved to a local path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Approximately 1MP images; prompt and optional aspect ratio; asynchronous generation is available.]

## Skill Version(s):

1.3.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
