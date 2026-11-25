## Description:

Separates an image's foreground from its background and returns a transparent-background image URL for product processing, portrait cutouts, and compositing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to remove image backgrounds for product photos, portrait cutouts, and compositing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reported a mismatch between the image-processing description and authentication commands, and its analysis was partial.

Mitigation: Review the CLI authentication and API-key setup to confirm they match the expected dLazy workflow before configuring credentials.

Risk: The skill documentation says local image inputs are uploaded to dLazy media storage for processing.

Mitigation: Submit only images you are authorized to share with the service.

## Reference(s):

- [ClawHub release](https://clawhub.ai/dlazyai/skills/dlazy-imageseg)
- [CLI repository (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Image, JSON, URLs]

**Output Format:** [JSON response containing a generated image URL, or an asynchronous task identifier when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are hosted by dLazy; the CLI can optionally save an output locally.]

## Skill Version(s):

1.3.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
