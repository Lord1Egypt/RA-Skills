## Description:

Image-to-SVG tool: converts raster images (PNG/JPG) into color vector SVG and returns the URL, suitable for lossless scaling and vectorization of logos, icons, and flat illustrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers can convert raster images such as logos, icons, and flat illustrations into vector artwork for scalable use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a mismatch between the image-conversion purpose and CLI login/authentication commands; the scan was partial and did not inspect the CLI package or authentication behavior.

Mitigation: Review the pinned CLI package and authentication flow before installing it or entering an API key.

Risk: Prompts and local images are sent to dLazy's hosted API and media storage.

Mitigation: Submit only images and prompts approved for processing by the service.

## Reference(s):

- [CLI repository (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON response containing a hosted result URL; asynchronous requests may return a task identifier.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes vector SVG conversion; the documented response example identifies its returned asset as image/png.]

## Skill Version(s):

1.2.40 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
