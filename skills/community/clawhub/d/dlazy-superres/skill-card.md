## Description:

Requests image super-resolution through dLazy's hosted service and returns a URL for the resulting image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams can use this skill to request higher-resolution versions of low-resolution images or restore image detail through dLazy's hosted service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and did not demonstrate the advertised image-upscaling capability.

Mitigation: Confirm the service behavior with a non-sensitive test image before relying on the result.

Risk: Local image files supplied for processing are uploaded to dLazy's hosted media service.

Mitigation: Only submit images you are comfortable sending to that service, and review its terms before processing sensitive material.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-superres)
- [CLI homepage (listed in metadata)](https://github.com/dlazy-ai/cli)
- [dLazy CLI package (listed in metadata)](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Image, URL, JSON]

**Output Format:** [JSON result containing a URL to the processed image]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The result image is hosted remotely; asynchronous requests may first return a task ID without an image output.]

## Skill Version(s):

1.3.42 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
