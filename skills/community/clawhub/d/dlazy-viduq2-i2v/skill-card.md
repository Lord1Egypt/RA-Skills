## Description:

Convert static images into dynamic videos with the Vidu Q2 image-to-video model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and agent users provide one or more images and a motion prompt to generate a Vidu Q2 video, with controls for framing, duration, resolution, and optional audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security scan was partial and did not fully resolve the referenced CLI package. The skill requires a dLazy API key and sends prompts and supplied media to dLazy's hosted service.

Mitigation: Review the pinned @dlazy/cli 1.2.3 package before installation, and submit only prompts and media you are comfortable sending to dLazy. Use a dedicated API key and rotate or revoke it when needed.

Risk: The security summary notes that the supplied instructions mainly document authentication rather than the advertised image-to-video workflow.

Mitigation: Check the CLI help and confirm its current generation behavior with a non-sensitive sample before relying on it.

## Reference(s):

- [dLazy CLI project (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [dLazy CLI npm package (listed in skill metadata)](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [JSON, Generated media URLs, Video files]

**Output Format:** [JSON response with generated media URLs and optional task status; media can also be saved as a local file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation options include reference-image or first/last-frame modes, duration, aspect ratio, resolution, and optional audio; asynchronous requests may return a task identifier before media is ready.]

## Skill Version(s):

1.3.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
