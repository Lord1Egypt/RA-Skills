## Description:

Generate and edit images with Nano Banana Pro using text prompts or reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other ClawHub users can generate images from prompts or edit existing images through dLazy's Nano Banana Pro service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a medium-confidence benign verdict but notes that the scan was partial, the pinned CLI install detail could not be resolved, and the reported login behavior is not clearly connected to the image features.

Mitigation: Review the pinned @dlazy/cli package and confirm its login behavior before installing or using it.

Risk: Prompts and local reference-image paths are sent to dLazy's hosted API and media storage.

Mitigation: Submit only content you are comfortable sharing with the service, protect the API key in local configuration, and rotate or revoke it if exposed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-banana-pro)
- [dLazy homepage](https://dlazy.com)
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli)
- [CLI repository link listed in skill metadata (provenance unavailable)](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Image files, JSON result metadata]

**Output Format:** [Image assets returned by URL, with JSON result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return an asynchronous task identifier when run without waiting.]

## Skill Version(s):

1.2.45 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
